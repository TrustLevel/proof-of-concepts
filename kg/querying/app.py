import time
from typing import List, Tuple

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv("../.env")
load_dotenv(".env")

from nlp import rewrite_query
from streamlit_agraph import Config, Edge, Node, agraph

from kg import fetch_articles_related_to_nodes
from ner import get_entities_from_text


def execute_query(query) -> Tuple[List[Node], List[Edge]]:
    rewritten_query = rewrite_query(query)
    st.write(f"Rewritten query for NER:\n{rewritten_query}")
    entities = get_entities_from_text(rewritten_query)
    if len(entities) == 0:
        st.error("No entities found. Please try to rewrite your query.")
        st.stop()
    st.write("Used entities for querying:")
    for entity in entities:
        st.write(f"- {entity.type}: {entity.text}")
    return fetch_articles_related_to_nodes(entities)


def draw_knowledge_graph(nodes: List[Node], edges: List[Edge]):
    config = Config(height=500, physics=True, hierarchical=False)
    config.onNodeClick = "function(node) { window.open('https://google.com', '_blasnk'); }"
    agraph(nodes=nodes, edges=edges, config=config)
# Streamlit UI
st.title('Knowledge Graph Query Executor')

query = st.text_input('Enter your query here:')
execute_button = st.button('Execute Query')

if execute_button:
    with st.spinner('Executing query...'):
        nodes, edges = execute_query(query)
        st.success('Query executed successfully!')

        st.subheader("Results:")
        if len(nodes) == 0 and len(edges) == 0:
            st.write("No Results found!. Maybe try to change your query?")
        draw_knowledge_graph(nodes, edges)
