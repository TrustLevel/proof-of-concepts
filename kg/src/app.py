from typing import List

import streamlit as st
from dotenv import load_dotenv

load_dotenv("../.env")
load_dotenv(".env")

from entity_recognition import (get_authors_and_publishers_from_text,
                                get_entities_from_text)
from graphdb import \
    fetch_articles_and_relations_for_entities_authors_and_publishers
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
        authors, publishers = get_authors_and_publishers_from_text(rewritten_query)

        if (len(entities) + len(authors) + len(publishers)) == 0:
            st.error("No entities, authors or publishers found. Please try to rewrite your query.")
            st.stop()

        st.write("Used entities for querying:")
        for entity in entities:
            st.write(f"- {entity.type}: {entity.text}")
        for author in authors:
            st.write(f"- Author: {author}")
        for publisher in publishers:
            st.write(f"- Publisher: {publisher}")

        articles, nodes, edges, = fetch_articles_and_relations_for_entities_authors_and_publishers(entities, authors, publishers)

        articles.sort(key=lambda article: article.trustlevel, reverse=True)

        st.success('Query executed successfully!')

        st.subheader("Results:")
        if len(nodes) == 0 and len(edges) == 0:
            st.write("No Results found!. Maybe try to change your query?")
        
        draw_knowledge_graph(nodes, edges)
        st.subheader("Displayed Articles:")
        max_columns_per_row = 3
        # Calculate the total number of rows needed
        total_rows = len(articles) // max_columns_per_row + (1 if len(articles) % max_columns_per_row else 0)

        for row in range(total_rows):
            # Calculate the start and end index for articles in the current row
            start_idx = row * max_columns_per_row
            end_idx = min(start_idx + max_columns_per_row, len(articles))
            # Create columns for the current row
            columns = st.columns(max_columns_per_row)
            for i, article in enumerate(articles[start_idx:end_idx]):
                with columns[i]:
                    container = st.container(border=True)
                    container.subheader(article.title)
                    mentioned_entities = ",".join(article.mentioned_entities)
                    container.write(f"Mentioned: {mentioned_entities}")
                    if article.author:
                        container.write(f"Author: {article.author}")
                    if article.publisher:
                        container.write(f"Publisher: {article.publisher}")
                    container.markdown(f"**Trustlevel**: {article.trustlevel}")
                    container.markdown(f'[Open]({article.url})', unsafe_allow_html=True)