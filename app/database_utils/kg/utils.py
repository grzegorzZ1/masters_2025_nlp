import os
import json
import numpy as np
import requests
import pandas as pd
from tqdm import tqdm
from sklearn.preprocessing import normalize

from extraction_prompts import (
    EXTRACT_RELATION_TRIPLETS_PROMPT,
    REFORMULATE_RELATION_TRIPLET,
    VALIDATE_TRIPLET_USEFULNESS,
    VALIDATE_TRIPLET_REFORMULATION,
    DECIDE_OUTLIER_FATE,
    FIND_BETTER_RELATION_NAME,
    VALIDATE_RELATION_NAME
)

def ollama_request(prompt, is_stream=False):
    payload = {
        "model": os.getenv("MODEL_NAME"),
        "prompt": prompt,
        "stream": is_stream,
    }
    if os.getenv("IS_IN_DOCKER", False):
        current_llama_host = os.getenv("DOCKER_LLAMA_HOST")
    else:
        current_llama_host = os.getenv("LOCAL_LLAMA_HOST")

    current_llama_uri = current_llama_host + "/api/generate"

    try:
        response = requests.post(
            current_llama_uri, json=payload, stream=is_stream
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def create_relations(es_client, fragment_index_name, step=2, reformulate=True):
    final_triplets = pd.DataFrame(columns=["speech_id", "start", "end", "date", "subject", "predicate", "object"])
    for speech_id in range(1, 999999):
        fragments_for_text = es_client.search(
            index=fragment_index_name,
            query={
                "match": {
                    "speech_id": speech_id
                }
            }
        )
        hits = fragments_for_text['hits']['hits']
        if len(hits) == 0:
            break
        
        for fragment_id in tqdm(range(0, len(hits), step), desc=f"Processing speech_id: {speech_id}"):
            fragment_group = hits[fragment_id:fragment_id + step]
            fragment_text = " ".join(
                hit["_source"]["text"]
                for hit in fragment_group
                if hit["_source"].get("text")
            )
            jsoned_triplets = None
            for attempt in range(2):
                triplets = ollama_request(
                    prompt=EXTRACT_RELATION_TRIPLETS_PROMPT.format(fragment=fragment_text, speech_author=fragment_group[0]["_source"].get("author", "Unknown")),
                    is_stream=False
                )
                try:
                    jsoned_triplets = json.loads(triplets)["triplets"]
                    break
                except json.JSONDecodeError as e:
                    if attempt == 0:
                        print(f"JSON decoding error for speech_id {speech_id}, fragment_id {fragment_id}, Retrying once with the same prompt...")
                    else:
                        continue

            if jsoned_triplets is None:
                continue

            for triplet in jsoned_triplets:
                if triplet is None or not isinstance(triplet, dict):
                    continue
                subject = triplet.get("subject", None)
                predicate = triplet.get("predicate", None)
                object_ = triplet.get("object", None)

                if any(not x for x in [subject, predicate, object_]):
                    continue

                reformulated_triplet = {}
                if reformulate:
                    for attempt in range(2):
                        try:
                            reformulated_triplet = json.loads(
                                ollama_request(
                                    prompt=REFORMULATE_RELATION_TRIPLET.format(subject=subject, predicate=predicate, object=object_),
                                    is_stream=False
                                )
                            )
                        except json.JSONDecodeError as e:
                            print(f"JSON decoding error during reformulation for speech_id {speech_id}, fragment_id {fragment_id}: {e}")
                            continue

                        if len(reformulated_triplet) > 0:
                            if any(not x for x in [reformulated_triplet.get("subject"), reformulated_triplet.get("predicate"), reformulated_triplet.get("object")]):
                                continue
                            is_reformulation_valid = ollama_request(
                                prompt=VALIDATE_TRIPLET_REFORMULATION.format(
                                    subject=subject,
                                    predicate=predicate,
                                    object=object_,
                                    reformulated_subject=reformulated_triplet.get("subject", subject),
                                    reformulated_predicate=reformulated_triplet.get("predicate", predicate),
                                    reformulated_object=reformulated_triplet.get("object", object_)
                                ),
                                is_stream=False
                            )

                            if is_reformulation_valid != "valid":
                                if attempt == 0:
                                    print(f"Reformulation of triplet: deemed invalid, Retrying once with the same prompt...")
                                else:
                                    continue

                reformulated_triplet = {
                    "subject": reformulated_triplet.get("subject", subject),
                    "predicate": reformulated_triplet.get("predicate", predicate),
                    "object": reformulated_triplet.get("object", object_)
                }
                
                is_valid = ollama_request(
                    prompt=VALIDATE_TRIPLET_USEFULNESS.format(
                        subject=reformulated_triplet.get("subject", subject),
                        predicate=reformulated_triplet.get("predicate", predicate),
                        object=reformulated_triplet.get("object", object_)
                    ),
                    is_stream=False
                )
                if is_valid != "useful":
                    print(f"Triplet: {reformulated_triplet.get('subject', subject)}, {reformulated_triplet.get('predicate', predicate)}, {reformulated_triplet.get('object', object_)} deemed not useful")
                    continue

                final_triplets = pd.concat([final_triplets, pd.DataFrame([{
                    "speech_id": speech_id,
                    "start": fragment_group[0]["_source"]["chunk_start"],
                    "end": fragment_group[-1]["_source"]["chunk_end"],
                    "date": fragment_group[0]["_source"]["date"],
                    "subject": reformulated_triplet.get("subject", subject).lower().strip(),
                    "predicate": reformulated_triplet.get("predicate", predicate).lower().strip(),
                    "object": reformulated_triplet.get("object", object_).lower().strip()
                }])], ignore_index=True)
    return final_triplets


def trimm_entities(triplets, embed_model, cluster_model, N=2):

    unique_entities = list(set(pd.concat([triplets["subject"], triplets["object"]]).dropna()))
    encoded_entities = embed_model.encode(unique_entities, normalize_embeddings=True).tolist()

    X = normalize(encoded_entities, norm="l2")
    cluster_labels = cluster_model.fit_predict(X)

    mapping = {}

    outliers = np.array(unique_entities)[np.where(cluster_labels == -1)[0]]
    for outlier in outliers:
        is_valid = ollama_request(
            prompt=DECIDE_OUTLIER_FATE.format(entity=outlier),
            is_stream=False
        )
        if is_valid == "valid":
            mapping[str(outlier)] = str(outlier)
        else:
            mapping[str(outlier)] = None

    for i in range(max(cluster_labels) + 1):
        cluster_indices = np.where(cluster_labels == i)[0]
        cluster_entities = np.array(unique_entities)[cluster_indices]
        encoded_cluster_entities = np.array(encoded_entities)[cluster_indices]
        cluster_mean = np.mean(encoded_cluster_entities, axis=0)
        distances = np.linalg.norm(encoded_cluster_entities - cluster_mean, axis=1)
        closest_entities = cluster_entities[distances <= min(distances)+(max(distances) - min(distances))/N]
        for attempt in range(2):
            better_relation_name = ollama_request(
                prompt=FIND_BETTER_RELATION_NAME.format(relation_list=closest_entities.tolist()),
                is_stream=False
            )

            is_valid_relation_name = ollama_request(
                prompt=VALIDATE_RELATION_NAME.format(relation_name=better_relation_name),
                is_stream=False
            )

            if is_valid_relation_name == "valid":
                for entity in cluster_entities:
                    mapping[str(entity)] = str(better_relation_name).replace('"', '').replace("'", "")
                break
            else:
                if attempt == 1:
                    for entity in cluster_entities:
                        mapping[str(entity)] = str(entity)

    # TODO: Based on mapping update the triplets dataframe to replace the entities with their mapped values and remove any triplets that have None as subject or object.