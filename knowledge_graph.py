import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import math  # For checking NaN

# Streamlit app title
st.title("Knowledge Graph: Articles, Authors, Publishers, and Entities")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload the CSV file containing articles with entities", type="csv")

# Helper function to safely handle NaN values and ensure strings
def safe_str(value):
    if pd.isna(value) or value == '' or value is None:
        return None
    return str(value)

# Function to build and visualize the knowledge graph
def create_knowledge_graph(df):
    # Create a NetworkX graph
    G = nx.Graph()

    # Add nodes and edges for each article
    for index, row in df.iterrows():
        article_node = safe_str(row['title'])
        author_node = safe_str(row['author'])
        publisher_node = safe_str(row['publisher'])

        if article_node is None or author_node is None or publisher_node is None:
            continue  # Skip rows with invalid data

        # Add nodes
        G.add_node(article_node, label="Article", title=article_node)
        G.add_node(author_node, label="Author", title=author_node)
        G.add_node(publisher_node, label="Publisher", title=publisher_node)

        # Add edges between the article and the author, publisher
        G.add_edge(article_node, author_node)
        G.add_edge(article_node, publisher_node)

        # Add entity nodes and edges for each entity type
        for entity_type in ["PERSON", "ORG", "GPE", "LOC", "DATE", "EVENT", "NORP", "PRODUCT"]:
            entity_column = safe_str(row[entity_type])
            if entity_column is not None:  # Check if the entity column exists
                entities = entity_column.split(", ")
                for entity in entities:
                    entity_node = safe_str(entity)
                    if entity_node is not None:
                        G.add_node(entity_node, label=entity_type, title=entity_node)
                        G.add_edge(article_node, entity_node)

    # Use pyvis to visualize the graph
    net = Network(height="600px", width="100%", notebook=False)
    net.from_nx(G)

    # Enable physics so that nodes have a natural layout
    net.show_buttons(filter_=['physics'])

    # Generate the HTML file to display the graph
    net.save_graph("knowledge_graph.html")
    return net

# Process the uploaded CSV file
if uploaded_file is not None:
    # Read the CSV file into a dataframe
    df = pd.read_csv(uploaded_file)

    # Display the full CSV
    st.subheader("Uploaded CSV Content")
    st.dataframe(df)

    # Create and visualize the knowledge graph
    st.subheader("Interactive Knowledge Graph")
    net = create_knowledge_graph(df)

    # Display the generated graph in the Streamlit app
    HtmlFile = open("knowledge_graph.html", 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=700)

else:
    st.info("Please upload the CSV file to generate the knowledge graph.")