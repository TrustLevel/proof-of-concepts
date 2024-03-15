from typing import List

import streamlit as st
from dotenv import load_dotenv

load_dotenv("../.env")
load_dotenv(".env")

from entity_recognition import get_entities_from_text
from graphdb import fetch_articles_and_relations_for_entities
from nlp import rewrite_query
from streamlit_agraph import Edge, Node


def draw_knowledge_graph(nodes: List[Node], edges: List[Edge]):
    from pyvis.network import Network
    from stvis import pv_static

    g = Network(height='500px', width='1000px', heading='')
    for node in nodes:
        g.add_node(node.id, label=node.label, title=node.title, color=node.color)
            
    for edge in edges:
        g.add_edge(edge.source, edge.to, title=edge.label, color=edge.color)

    pv_static(g)

st.title('Knowledge Graph Query Executor')

query = st.text_input('Enter your query here:')
execute_button = st.button('Execute Query')

if execute_button:
    with st.spinner('Executing query...'):
        rewritten_query = rewrite_query(query)
        st.write(f"Rewritten query for NER:\n{rewritten_query}")
        
        entities = get_entities_from_text(rewritten_query)
        if len(entities) == 0:
            st.error("No entities found. Please try to rewrite your query.")
            st.stop()
        st.write("Used entities for querying:")
        for entity in entities:
            st.write(f"- {entity.type}: {entity.text}")

        articles, nodes, edges, = fetch_articles_and_relations_for_entities(entities)

        st.success('Query executed successfully!')

        st.subheader("Results:")
        if len(nodes) == 0 and len(edges) == 0:
            st.write("No Results found!. Maybe try to change your query?")
        
        draw_knowledge_graph(nodes, edges)
        st.subheader("Displayed Articles:")
        columns = st.columns(len(articles))
        for i, article in enumerate(articles):
            with columns[i]:
                container = st.container(border=True)
                container.subheader(article.title)
                mentioned_entities = ",".join(article.mentioned_entities)
                container.write(f"Mentioned: {mentioned_entities}")
                container.markdown(f"**Trustlevel**: {article.trustlevel}")
                container.markdown(f'[Open]({article.url})', unsafe_allow_html=True)
