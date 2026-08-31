import spacy
import networkx as nx
import itertools
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

from workers.worker_classes.results_workers.ResultsWorkerModule import ResultsWorker


class SocialNetworkWorker(ResultsWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance, index_name, data=None):
        super().work(task_instance, index_name, data=data)

        if "vizualization" not in st.session_state:
            G = self._build_entity_proximity_graph(
                self.data,
                task_instance.terms,
                window_size=task_instance.window_size
            )
            st.session_state["vizualization"] = G
        else:
            G = st.session_state["vizualization"]

        self._visualize_graph(G, task_instance.terms, task_instance.minimum_edge_weight)


    def _extract_entities(self, doc, input_terms, proximity_window=5):
        input_terms_norm = [t.lower().strip() for t in input_terms.split(",")]

        main_entities = []
        other_entities = []
        for ent in doc.ents:
            ent_text = ent.text.strip().lower()
            entry = {"text": ent_text, "start": ent.start, "end": ent.end - 1}
            if ent_text in input_terms_norm:
                main_entities.append(entry)
            else:
                other_entities.append(entry)

        if not main_entities:
            return []

        print(f"Main entities: {main_entities}")
        print(f"Other entities: {other_entities}")
        entities = list(main_entities)
        for ent in other_entities:
            for main in main_entities:
                distance = min(
                    abs(ent["start"] - main["end"]),
                    abs(main["start"] - ent["end"])
                )
                if distance <= proximity_window:
                    entities.append(ent)
                    break

        return entities


    def _build_entity_proximity_graph(self, docs, input_terms, window_size=5):
        nlp = spacy.load("en_core_web_sm")
        G = nx.Graph()

        for doc in docs:
            doc_id = doc["_id"]
            src = doc["_source"]
            text = src.get("text", "")
            doc = nlp(text)
            entities = self._extract_entities(doc, input_terms, proximity_window=window_size)
            for ent in entities:
                if not G.has_node(ent["text"]):
                    G.add_node(ent["text"], node_type="entity")

            for e1, e2 in itertools.combinations(entities, 2):
                if e1["text"] == e2["text"]:
                    continue

                distance = min(
                    abs(e2["start"] - e1["end"]),
                    abs(e1["start"] - e2["end"])
                )

                if distance <= window_size:
                    a, b = sorted([e1["text"], e2["text"]])

                    if G.has_edge(a, b):
                        G[a][b]["weight"] += 1
                        G[a][b]["docs"].add(doc_id)
                    else:
                        G.add_edge(
                            a,
                            b,
                            weight=1,
                            docs={doc_id},
                        )

        return G
    
    def _visualize_graph(self, G, input_terms, min_weight=2):
        input_terms_norm = {t.lower().strip() for t in input_terms.split(",")}

        filtered_edges = [(u, v, d) for u, v, d in G.edges(data=True) if d["weight"] > min_weight]
        visible_nodes = set()
        for u, v, _ in filtered_edges:
            visible_nodes.add(u)
            visible_nodes.add(v)

        nodes = []
        for node in visible_nodes:
            is_main = node.lower() in input_terms_norm
            nodes.append(Node(
                id=node,
                label=node,
                size=15 if is_main else 6,
                color="#ff6b6b" if is_main else "#4ecdc4",
            ))

        edges = []
        for u, v, data in filtered_edges:
            edges.append(Edge(
                source=u,
                target=v,
                label=str(data["weight"]),
                width=0.1 + data["weight"],
                color="rgba(150,150,150,0.6)",
            ))

        config = Config(
            width=800,
            height=600,
            directed=False,
            physics=True,
            hierarchical=False,
        )

        agraph(nodes=nodes, edges=edges, config=config)

    def _create_query(self, task_instance):
        terms = [t.strip() for t in task_instance.terms.split(",")]
        query = {
            "bool": {
                "must": [
                    {
                        "range": {
                            "date": {
                                "gte": "-".join(task_instance.min_date.split("-")[::-1]),
                                "lte": "-".join(task_instance.max_date.split("-")[::-1])
                            }
                        }
                    },
                    {
                        "bool": {
                            "should": [{"match": {"text": term}} for term in terms],
                            "minimum_should_match": 1
                        }
                    }
                ]
            }
        }
        return query

    def _prepare_final_data(self):
        final_data = []
        for doc in self.data:
            final_data.append(doc["_source"]["text"])
        
        return final_data