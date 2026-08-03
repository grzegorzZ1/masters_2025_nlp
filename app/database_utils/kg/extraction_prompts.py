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
Note that the subject and object should be valid and concrete entities in a most concise and clear format and must be identifiable as a specific political entity.
Return only a valid JSON object. Do not include any additional text, explanations, or symbols.
"""

REFORMULATE_RELATION_TRIPLET = """
You are a relation extraction model specialized in extracting political relations between political entities.
Your task is to reformulate the given relation triplet.
Make sure subject and object are valid and concrete entities in a most concise and clear format related to politics, either inside (political party, government official) or outside the country (foreign government, international organization, other countries).
Predicate should be a clear and very concise, best one word meaning the relationship between the subject and object.
The most important is to not change meaning of relation between subject and object, but to make it more clear and concise with a single word if possible.
The triplet is: subject: {subject}, predicate: {predicate}, object: {object}.

Return answer in the following JSON format:
{{
    "subject": "...",
    "predicate": "...",
    "object": "..."
}}
Do not include any additional text, explanations, or symbols.
"""

VALIDATE_TRIPLET_USEFULNESS = """
You are a political scientist model.
Your task is to validate the given relation triplet in case of the usefulness in your political analysis.
A relation triplet consists of a subject, a predicate, and an object.
The triplet is: subject: {subject}, predicate: {predicate}, object: {object}.
Think if subject and obejct are valid entities in a most concise and clear format related to politics, either inside (political party, government official) or outside the country (foreign government, international organization, other countries).
Think if predicate is a relation between subject and object which make sense and might be useful for political text analysis.
Return a single word "useful" if the triplet is useful for political text analysis, or "not_useful" if it is not useful.
Do not include any additional text, explanations, or symbols.
"""

VALIDATE_TRIPLET_REFORMULATION = """
You are a political scientist model.
I have two sets of relation triplets. First was extracted from the text, and second was reformulated by a relation extraction model.
Your task is to validate if the reformulation of the triplet is valid and does not change the meaning of the relation between subject and object.
The first triplet is: subject: {subject}, predicate: {predicate}, object: {object}.
The second triplet is: subject: {reformulated_subject}, predicate: {reformulated_predicate}, object: {reformulated_object}.
Return a single word "valid" if the reformulation is valid and does not change the meaning of the relation between subject and object, or "invalid" if it is not valid.
You don't need to be very strict, if the reformulation is not perfect but still does not change the meaning of the relation between subject and object, consider it as valid.
Do not include any additional text, explanations, or symbols.
"""

DECIDE_OUTLIER_FATE = """
You are a political scientist model.
I am building a political knowledge graph from political speeches.
I have an entitiy extracted from the speeches.
Decide whether this entity is a valid political entity or not.
The entity is: {entity}.
Return a single word "valid" if the entity is a valid political entity, or "invalid" if it is not valid.
Do not include any additional text, explanations, or symbols.
"""

FIND_BETTER_RELATION_NAME = """
You are a political scientist model.
I have a relation name extracted from political speeches.
You will be given a list of similar relation names extracted from the speeches.
Your task is to find a single relation name that is the most clear and concise, and best replaces all the other relation names in the list.
The relation list is: {relation_list}.
Return a single relation name that is the most clear and concise, and best replaces all the other relation names in the list.
Do not include any additional text, explanations, or symbols.
"""

VALIDATE_RELATION_NAME = """
You are a political scientist model.
I have a relation name extracted from political speeches.
Your task is to validate if the relation name is clear and concise, and if it makes sense as a relation between political entities.
The relation name is: {relation_name}.
Return a single word "valid" if the relation name is clear and concise, and makes sense as a relation between political entities, or "invalid" if it is not valid.
Do not include any additional text, explanations, or symbols.
"""