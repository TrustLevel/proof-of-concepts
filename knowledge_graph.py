import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# Streamlit app title
st.title("Knowledge Graph: Articles, Authors, Publishers, and Entities")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload the CSV file containing articles with entities", type="csv")

# Function to build and visualize the knowledge graph
def create_knowledge_graph(df):
    # Create a NetworkX graph
    G = nx.Graph()

    # Add nodes and edges for each article
    for index, row in df.iterrows():
        article_node = row['title']
        author_node = row['author']
        publisher_node = row['publisher']

        # Add nodes
        G.add_node(article_node, label="Article", title=article_node)
        G.add_node(author_node, label="Author", title=author_node)
        G.add_node(publisher_node, label="Publisher", title=publisher_node)

        # Add edges between the article and the author, publisher
        G.add_edge(article_node, author_node)
        G.add_edge(article_node, publisher_node)

        # Add entity nodes and edges for each entity type
        for entity_type in ["PERSON", "ORG", "GPE", "LOC", "DATE", "EVENT", "NORP", "PRODUCT"]:
            if pd.notnull(row[entity_type]):  # Check if there are entities of this type
                entities = row[entity_type].split(", ")
                for entity in entities:
                    G.add_node(entity, label=entity_type, title=entity)
                    G.add_edge(article_node, entity)

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
