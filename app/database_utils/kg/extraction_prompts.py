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

- Subject and object must be politically relevant entities or concepts.
- They may include countries, people, governments, institutions, parties,
  organizations, political groups, laws, policies, rights, reforms,
  political issues, security issues, or territories.
- Avoid only clearly useless references such as pronouns, "someone",
  "something", "everyone", or phrases with no identifiable meaning.
- Extract only relations explicitly stated in the fragment.
- Keep names close to how they appear in the text.
- Keep different entities separate.
- Use a short verb phrase as the predicate.
- Preserve negation and modality.
- Do not extract duplicate relations.

PRONOUNS:

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

VALIDATE_TRIPLET_USEFULNESS = """
Decide if this triplet is potentially useful for a political knowledge graph.

Return exactly:
useful
or
not_useful

Triplet:
subject: {subject}
predicate: {predicate}
object: {object}

Return useful if:

- subject and object are meaningful political entities, groups, institutions,
  places, laws, policies, issues, rights, reforms, or other political concepts;
- predicate expresses a clear relation or action;
- the triplet makes reasonable sense on its own.

Return not_useful only if:

- subject or object is clearly meaningless, unresolved, or only a pronoun;
- predicate does not express a real relation;
- predicate only means mentioning, discussing, saying, or thinking;
- the triplet is malformed or makes no sense.

Do not reject a triplet only because an entity is broad or abstract.

If uncertain, prefer useful.

Return only useful or not_useful.
Do not include any additional text, explanations, or symbols.
Do not return any code, punctuation, or quotation marks.
"""

DECIDE_OUTLIER_FATE_ENTITY = """
Classify the candidate as valid or invalid.

Candidate:
<entity>{outlier}</entity>

valid:
A meaningful noun or noun phrase useful in a political knowledge graph.
It may describe a political actor, institution, country, government body,
office, law, right, policy, security issue, diplomatic issue, public issue,
or political concept.

invalid:
A pronoun, vague reference, verb phrase, complete sentence, quotation,
instruction, time expression, malformed phrase, or clearly irrelevant object.

Keep potentially useful political nodes.
Reject only clearly unusable extractions.

Return format:
Return exactly one string: valid or invalid.
Do not repeat the candidate.
Do not provide an explanation.
Do not include code, punctuation, or quotation marks.
"""

DECIDE_OUTLIER_FATE_RELATION = """
Classify the candidate as valid or invalid.

Candidate:
<relation>{outlier}</relation>

valid:
A meaningful verb or verb phrase useful as a relation in a political knowledge graph.
It may describe an action, position, cooperation, conflict, membership,
responsibility, legal relation, diplomatic relation, communication, or other
connection between two nodes. It may be negated or passive.

invalid:
A noun or topic, entity name, long fragment, complete sentence, quotation, or text that does not express a relation.

Keep potentially useful relations.

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

VALIDATE_ENTITY_NAME = """
Decide if the candidate is a valid name for a political knowledge-graph node.

Return exactly:
valid
or
invalid

Candidate:
{name}

Return valid if the candidate:

- is a concise noun or noun phrase;
- represents one clear political entity or concept;
- makes sense without extra context;

Return invalid if it:

- is a pronoun or vague reference;
- is an action or relation phrase;
- is a sentence or quotation;
- contains several separate entities;
- is too vague or malformed;
- is an overly long description.

Do not rewrite the candidate.

If uncertain, return invalid.

Return only valid or invalid. Do not include any additional text, explanations, or symbols.
"""

VALIDATE_RELATION_NAME = """
Decide if the candidate is a good reusable relation name for a knowledge graph.

Return exactly:
valid
or
invalid

Candidate:
{name}

Return valid if it:

- is a verb or verb phrase;
- expresses one clear relation;
- works as: SUBJECT + relation + OBJECT;
- is concise and reusable;


Return invalid if it:

- is a noun or topic;
- is only a vague verb such as "is", "has", or "does";
- contains several relations;
- contains its own subject or object;
- needs missing context;
- only reports speech, such as "said";
- is malformed.

Negated and passive relations are valid.

If uncertain, return invalid.

Return only valid or invalid. Do not rewrite the candidate, include any additional text, explanations, or symbols.
"""

REFORMULATE_RELATION_TRIPLET = """
Rewrite the predicate as a clear and concise relation.

Predicate:
{predicate}

Rules:
- Keep the original meaning.
- Make it as short as possible.
- Prefer one verb or a short verb phrase.
- Preserve negation and modality.
- The predicate must describe only the relation.
- Do not include any entity, person, country, organization, institution, or proper name.
- Do not include the subject or object inside the predicate.
- Remove entity-specific details that are not part of the relation.
- Do not add new information.

Good:
supports
opposes
cooperates with
is a member of
does not recognize
imposed sanctions on

Bad:
supports Russia
met with NATO
criticized the United States
Russia supports
cooperates with China

Return only the rewritten predicate as plain text.
Do not use JSON, quotes, explanations, or additional text.
"""