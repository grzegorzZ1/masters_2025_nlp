import spacy
from typing import List
import numpy as np
import os
import json
from tqdm import tqdm
import hashlib


from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

INDEX_NAME = os.getenv("INDEX_NAME")
FRAGMENTS_INDEX = f"{INDEX_NAME}_fragments"
EMBEDDING_SIZE = 384

PRONOUN_LINK_WORDS = {
    "it", "its", "itself",
    "they", "them", "their", "theirs", "themselves",
    "he", "him", "his", "himself",
    "she", "her", "hers", "herself",
    "this", "that", "these", "those",
    "each", "other", "another",
    "someone", "somebody", "something",
    "anyone", "anybody", "anything",
    "everyone", "everybody", "everything",
    "noone", "nobody", "nothing",
    "such", "same", "former", "latter",
    "which", "who", "whom", "whose",
}

MAPPING = {
    "properties": {
        "id":   {"type": "integer"},
        "unique_hash": {"type": "text"},
        "title": {"type": "text"},
        "place": {"type": "text"},
        "title_embedding": {
            "type": "dense_vector",
            "dims": EMBEDDING_SIZE,
            "index": True,
            "similarity": "cosine",
        },
        "text":  {"type": "text"},
        "date": {"type": "date"},
    }
}

FRAGMENTS_MAPPING = {
    "properties": {
        "id":   {"type": "integer"},
        "speech_id": {"type": "integer"},
        "chunk_position": {"type": "integer"},
        "unique_hash": {"type": "text"},
        "transcript_unfiltered": {"type": "text"},
        "text":  {"type": "text"},
        "date": {"type": "date"},
        "embedding": {
            "type": "dense_vector",
            "dims": EMBEDDING_SIZE,
            "index": True,
            "similarity": "cosine",
        },
    }
}

def segment_speech(
    text: str,
    *,
    semantic_threshold: float = 0.4,
    entity_weight: float = 0.12,
    lexical_weight: float = 0.05,
    max_fragment_sentences: int = 12,
):
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

    def entity_set(sent_span):
        return {ent.text.lower() for ent in sent_span.ents}

    def lexical_set(sent_span):
        return {tok.lower_ for tok in sent_span if tok.is_alpha and not tok.is_stop}

    def jaccard(a, b):
        if not a and not b:
            return 0.0
        return len(a & b) / max(1, len(a | b))



    def is_referential_token(tok):
        if tok.lower_ in PRONOUN_LINK_WORDS and tok.pos_ in {"PRON", "DET"}:
            return True

        return False

    def referential_subject_in_next(next_span):
        sent_tokens = [t for t in next_span if not t.is_space]
        if not sent_tokens:
            return False

        first = sent_tokens[0]
        if is_referential_token(first):
            return True
        for tok in next_span:
            if is_referential_token(tok) and tok.dep_ in {"nsubj", "nsubjpass", "expl"}:
                return True
        for tok in sent_tokens[:6]:
            if is_referential_token(tok) and (tok.dep_ in {"nsubj", "nsubjpass", "expl"} or tok == sent_tokens[0]):
                return True

        return False

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sent_spans = [s for s in doc.sents if s.text and s.text.strip()]
    if not sent_spans:
        return []

    sentences = [s.text.strip() for s in sent_spans]

    embeddings = model.encode(sentences, normalize_embeddings=True)

    entity_sets = [entity_set(s) for s in sent_spans]
    lexical_sets = [lexical_set(s) for s in sent_spans]

    fragments: List[List[str]] = []
    fragment_ranges: List[tuple] = []
    current_sents = [sentences[0]]
    current_start_index = 0
    current_emb = embeddings[0].copy()
    current_entities = set(entity_sets[0])
    current_lex = set(lexical_sets[0])

    for i in range(1, len(sentences)):
        sem = float(cos_sim(current_emb, embeddings[i]))
        ent_ol = jaccard(current_entities, entity_sets[i])
        lex_ol = jaccard(current_lex, lexical_sets[i])

        score = sem + entity_weight * ent_ol + lexical_weight * lex_ol
        continue_fragment = score >= semantic_threshold

        if not continue_fragment:
            next_span = sent_spans[i]
            if referential_subject_in_next(next_span):
                continue_fragment = True

        if len(current_sents) >= max_fragment_sentences:
            continue_fragment = False

        if continue_fragment:
            current_sents.append(sentences[i])
            current_entities |= entity_sets[i]
            current_lex |= lexical_sets[i]

            current_emb = (current_emb * (len(current_sents) - 1) + embeddings[i]) / len(current_sents)
            n = np.linalg.norm(current_emb)
            if n:
                current_emb = current_emb / n
        else:
            fragments.append(current_sents)
            fragment_ranges.append((current_start_index, i - 1))
            current_sents = [sentences[i]]
            current_start_index = i
            current_emb = embeddings[i].copy()
            current_entities = set(entity_sets[i])
            current_lex = set(lexical_sets[i])

    fragments.append(current_sents)
    fragment_ranges.append((current_start_index, len(sentences) - 1))
    joined_fragments = [" ".join(fragment) for fragment in fragments]
    return joined_fragments, fragment_ranges

def load_nlp_model(model_name):
    from spacy import load
    nlp = load(model_name)
    return nlp

def create_fragments_index(es_client, dataset_path: str, n_speeches: int = -1):
    nlp = load_nlp_model("en_core_web_sm")

    with open(dataset_path, "r") as f:
        speeches = json.load(f)


    for idx_name in [INDEX_NAME, FRAGMENTS_INDEX]:
        try:
            es_client.indices.delete(index=idx_name)
        except:
            print(f"Index {idx_name} does not exist yet")


    es_client.indices.create(index=INDEX_NAME, mappings=MAPPING)
    es_client.indices.create(index=FRAGMENTS_INDEX, mappings=FRAGMENTS_MAPPING)

    embed_model = SentenceTransformer("all-MiniLM-L6-v2", device=os.getenv("MODEL_DEVICE", "cpu"))

    speech_id = 0
    frag_id = 0
    count = 0
    for doc in tqdm(speeches, "Indexing..."):
        count += 1
        if count > n_speeches and n_speeches != -1:
            break
        speech_id += 1
        subset_speech = {k: doc[k] for k in doc.keys() if k in ["date", "title", "place", "transcript_filtered"]}
        transcript_unfiltered = doc.get("transcript_unfiltered", "")
        speech_author = transcript_unfiltered.split(":", 1)[0].strip()
        subset_speech["text"] = subset_speech.pop("transcript_filtered")
        if len(subset_speech["text"]) < 10:
            continue
        subset_speech["unique_hash"] = hashlib.sha256(subset_speech["text"].encode()).hexdigest()[:8]
        subset_speech["title_embedding"] = embed_model.encode(subset_speech["title"], normalize_embeddings=True).tolist()
        es_client.index(index=INDEX_NAME, id=speech_id, document=subset_speech)
        
        fragments, fragment_ranges = segment_speech(subset_speech["text"])
        for idx, fragment in enumerate(fragments):
            frag_id += 1
            embedding = embed_model.encode(fragment, normalize_embeddings=True).tolist()
            start_idx, end_idx = fragment_ranges[idx]
            frag_doc = {
                "speech_id": speech_id,
                "chunk_start": start_idx,
                "chunk_end": end_idx,
                "title": subset_speech.get("title", ""),
                "date": subset_speech.get("date", None),
                "unique_hash": hashlib.sha256(fragment.encode()).hexdigest()[:8],
                "text": fragment,
                "embedding": embedding,
            }
            if speech_author and len(speech_author) < 100:
                frag_doc["author"] = speech_author
            es_client.index(index=FRAGMENTS_INDEX, id=frag_id, document=frag_doc)


    print(f"Indexed {speech_id} speeches into '{INDEX_NAME}'")
    print(f"Indexed {frag_id} fragments into '{FRAGMENTS_INDEX}'")


    descriptions_path = "../../" + os.getenv("DATASET_DESCRIPTIONS")

    with open(descriptions_path, "r") as f:
        descriptions = json.load(f)

    descriptions[INDEX_NAME] = [f"Base dataset: {INDEX_NAME}"]
    descriptions[FRAGMENTS_INDEX] = [f"Base dataset: {FRAGMENTS_INDEX}"]

    with open(descriptions_path, 'w') as file:
        json.dump(descriptions, file)