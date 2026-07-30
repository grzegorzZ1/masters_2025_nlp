
import os
import json
from pydoc import doc, text
import requests
import spacy

from extraction_prompts import EXTRACT_RELATION_TRIPLETS_PROMPT

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

def create_relations(es_client, fragment_index_name, step=2):
    final_triplets = []
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
        
        for fragment_id in range(0, len(hits), step):
            print(f"Processing speech_id: {speech_id}, fragment_id: {fragment_id}-{min(len(hits), (fragment_id + step - 1))}/{len(hits)}")
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
                subject = triplet.get("subject", None)
                predicate = triplet.get("predicate", None)
                object_ = triplet.get("object", None)

                if any(not x for x in [subject, predicate, object_]):
                    continue

                # TODO: Validate a triplet

                final_triplets.append({
                    "speech_id": speech_id,
                    "start": fragment_group[0]["_source"]["chunk_start"],
                    "end": fragment_group[-1]["_source"]["chunk_end"],
                    "date": fragment_group[0]["_source"]["date"],
                    "subject": subject,
                    "predicate": predicate,
                    "object": object_
                })
    return final_triplets
