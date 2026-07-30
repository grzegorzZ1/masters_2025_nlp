EXTRACT_RELATION_TRIPLETS_PROMPT = """
You are a relation extraction model specialized in extracting political relations between political entities.
Your task is to extract a relation triplets from the given text.
A relation triplet consists of a subject, a predicate, and an object.
The subject and object are entities, and the predicate describes the relationship between them.
Return your answer in the following serializable JSON format:
{{
    "triplets": [
        {{
            "subject": "...",
            "predicate": "...",
            "object": "..."
        }},
        ...
    ]
}}

The text is: {fragment}

Since we are considering political speeches make sure each entity is an entity relevant to politics, either inside (political party, government official) or outside the country (foreign government, international organization, other countries).
Note that author of this speech is {speech_author}. You can consider it as a subject or object in the triplet.

Return only a valid JSON object. Do not include any additional text or explanations.
"""