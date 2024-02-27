import streamlit as st

from ner import extract_entities
from scraper import scrape_text


def process_url(url):
    return extract_entities(scrape_text(url))

# Streamlit UI
st.title("Article Entity Extractor")

# Button for loading the example URL
if st.button('Load Example URL'):
    # Update the URL in the session state
    st.session_state.url = "https://sputnikglobe.com/20231203/palestinian-leader-calls-on-icc-to-speed-up-israeli-war-crimes-trial--reports-1115353279.html"

# Use session state to hold the URL
url = st.text_input("Enter a URL:", key="url")

if url:
    # Display a message while processing
    with st.spinner('Processing...'):
        entities = process_url(url)
    
    # Once processing is done, prepare data for display
    data = [(entity, ', '.join(values)) for entity, values in entities.items()]
    
    # Display results as a table
    st.table(data)
