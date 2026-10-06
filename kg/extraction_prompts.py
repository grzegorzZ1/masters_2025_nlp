EXTRACT_RELATION_TRIPLETS_PROMPT = """
Extract political relations from the speech fragment.

Return only valid JSON:

{{
  "triplets": [
    {{
      "subject": "entity",
      "predicate": "relation",
      "object": "entity"
    }}
  ]
}}

If there are no relations, return:
{{"triplets": []}}

RULES:

- Subject and object must be short, relevant entities or concepts.
- Predicate must be a short, clear relation between them.
- Replace "I", "me", or "my" with "{speech_author}".
- Resolve other pronouns only when their meaning is clear.
- Otherwise, skip relations that depend on them.
- Use the speech author only when the author participates in the relation.

Extract at most 10 relations.

Speech author:
{speech_author}

Fragment:
{fragment}

Return only JSON.
Do not include any additional text, explanations, or symbols.
Do not return any code, punctuation, or quotation marks.
"""

DECIDE_OUTLIER_FATE_ENTITY = """
Classify the candidate as valid or invalid.

Candidate: {outlier}

valid:
A meaningful noun or noun phrase useful in a political knowledge graph.
It may describe a political actor, institution, country, government body,
office, law, right, policy, security issue, diplomatic issue, public issue,
or political concept.

invalid:
A pronoun, vague reference, verb phrase, complete sentence, quotation,
instruction, time expression, malformed phrase, or clearly irrelevant object.

Reject only clearly unusable extractions.

Return format:
Return exactly one string: valid or invalid.
Do not repeat the candidate.
Do not provide an explanation.
Do not include code, punctuation, or quotation marks.
"""

DECIDE_OUTLIER_FATE_RELATION = """
Classify the candidate as valid or invalid.

Candidate: {outlier}

valid:
A meaningful verb or verb phrase useful as a relation in a political knowledge graph.
It may describe an action, position, cooperation, conflict, membership,
responsibility, legal relation, diplomatic relation, communication, or other
connection between two nodes. It may be negated or passive.

invalid:
A noun or topic, entity name, long fragment, complete sentence, quotation, or text that does not express a relation.
Long and complex relations should be considered invalid.

Return format:
Return exactly one string: valid or invalid.
Do not repeat the candidate.
Do not provide an explanation.
Do not include code, punctuation, or quotation marks.
"""

FIND_BETTER_ENTITY_NAME = """
You are a political scientist model.
I have an entity name extracted from political speeches.
You will be given a list of similar entity names extracted from the speeches.
Your task is to find a single entity name that is the most clear and concise, and best replaces all the other entity names in the list.
The entity list is: {list}.
Return a single entity name that is the most clear and concise, and best replaces all the other entity names in the list.
If you think that entites from list are not similar or the same type, return "do_not_merge".
Do not include any additional text, explanations, or symbols.
"""


FIND_BETTER_RELATION_NAME = """
You are a political scientist model.
I have a relation predicate extracted from political speeches.
You will be given a list of similar relation predicates extracted from the speeches.
Your task is to find a single relation predicate that is the most clear and concise, and best replaces all the other relation predicates in the list.
The relation predicate list is: {list}.
Return a single relation predicate that is the most clear and concise, and best replaces all the other relation predicates in the list.
If you think that entites from list are not similar or the same type, return "do_not_merge".
Do not include any additional text, explanations, or symbols.
"""

REFORMULATE_RELATION_TRIPLET = """
Rewrite the predicate as a clear and concise relation.

Predicate:
{predicate}

Rules:
- Keep the original meaning.
- Make it as short as possible.
- Prefer one verb or a short verb phrase.
- The predicate must describe only the relation.
- Do not include any entities.
- Do not add new information.

Return only the rewritten predicate as plain text.
Do not use JSON, quotes, explanations, or additional text.
"""

NATURAL_LANGUAGE_PROMPT = """
Change the following information triplet into a natural language sentence.
Do not add any additional information.

triplet: {triplet}
"""