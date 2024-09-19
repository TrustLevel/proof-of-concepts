import streamlit as st
import pandas as pd
import spacy

# Load spaCy model for English
nlp = spacy.load("en_core_web_sm")

# Define entity types to filter
ENTITY_TYPES = ["PERSON", "ORG", "GPE", "LOC", "DATE", "EVENT", "NORP", "PRODUCT"]

# Streamlit app title
st.title("News Article Entity Extractor")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload a CSV file containing news articles", type="csv")

# Function to extract entities from text
def extract_entities(text):
    doc = nlp(text)
    entities = {entity_type: [] for entity_type in ENTITY_TYPES}  # Create empty lists for each entity type
    for ent in doc.ents:
        if ent.label_ in ENTITY_TYPES:
            entities[ent.label_].append(ent.text)
    return entities

# Display the extracted entities in a structured format
def display_entities(entities):
    for entity_type, entity_list in entities.items():
        if entity_list:
            st.markdown(f"**{entity_type}:** {', '.join(set(entity_list))}")

# Process the uploaded CSV file
if uploaded_file is not None:
    # Read the CSV file into a dataframe
    df = pd.read_csv(uploaded_file)

    # Display the full CSV
    st.subheader("Uploaded CSV Content")
    st.dataframe(df)

    # Process each article and extract entities
    st.subheader("Named Entities Extracted from Articles")

    # Ensure 'title' and 'text' columns exist
    if 'title' in df.columns and 'text' in df.columns:
        for index, row in df.iterrows():
            st.write(f"**Article {index + 1}:** {row['title']}")
            text = f"{row['title']} {row['text']}"  # Combine title and text for NER
            entities = extract_entities(text)
            display_entities(entities)
            st.markdown("---")  # Separator between articles
    else:
        st.error("The CSV file must contain 'title' and 'text' columns.")
