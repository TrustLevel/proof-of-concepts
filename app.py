import streamlit as st
import pandas as pd
import spacy
from io import StringIO

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

# Function to convert the list of entities to a comma-separated string
def convert_entities_to_string(entities):
    return {entity_type: ', '.join(set(entity_list)) for entity_type, entity_list in entities.items()}

# Process the uploaded CSV file
if uploaded_file is not None:
    # Read the CSV file into a dataframe
    df = pd.read_csv(uploaded_file)

    # Display the full CSV
    st.subheader("Uploaded CSV Content")
    st.dataframe(df)

    # Create a DataFrame to store entities for each article
    # We add author, publisher, and trust_score to the list of columns
    extracted_entities_df = pd.DataFrame(columns=['title', 'author', 'publisher', 'trust_score'] + ENTITY_TYPES)

    # Process each article and extract entities
    st.subheader("Named Entities Extracted from Articles")

    # Ensure 'title', 'text', 'author', 'publisher', and 'trust_score' columns exist
    if all(col in df.columns for col in ['title', 'text', 'author', 'publisher', 'trust_score']):
        for index, row in df.iterrows():
            st.write(f"**Article {index + 1}:** {row['title']}")
            text = f"{row['title']} {row['text']}"  # Combine title and text for NER
            entities = extract_entities(text)
            
            # Convert the entities to a comma-separated string for display
            string_entities = convert_entities_to_string(entities)
            
            # Add the title, author, publisher, trust_score, and entities to the DataFrame for spreadsheet export
            row_data = {
                'title': row['title'],
                'author': row['author'],
                'publisher': row['publisher'],
                'trust_score': row['trust_score']
            }
            row_data.update(string_entities)
            extracted_entities_df = extracted_entities_df.append(row_data, ignore_index=True)

            # Display the entities in the app
            for entity_type, entity_list in string_entities.items():
                if entity_list:
                    st.markdown(f"**{entity_type}:** {entity_list}")
            st.markdown("---")  # Separator between articles

        # Display the extracted entities DataFrame
        st.subheader("Extracted Entities Table")
        st.dataframe(extracted_entities_df)

        # Provide an option to download the DataFrame as a CSV file
        csv = extracted_entities_df.to_csv(index=False)
        st.download_button(
            label="Download Extracted Entities as CSV",
            data=csv,
            file_name='extracted_entities.csv',
            mime='text/csv',
        )
    else:
        st.error("The CSV file must contain 'title', 'text', 'author', 'publisher', and 'trust_score' columns.")
