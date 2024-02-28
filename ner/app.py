import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from nlp import rewrite_query
from scraper import scrape_text

from ner import extract_entities


def is_url(input_string):
    return input_string.startswith('http://') or input_string.startswith('https://')

def process_input(input_type, input_data):
    if input_type == 'URL':
        text = scrape_text(input_data)
        st.text_area("Extracted text:", value=text, height=100, disabled=True)
    elif input_type == 'User Query':
        text = rewrite_query(input_data)
        st.text_area("Rewritten Query (optimized for entity extraction):", value=text, height=50, disabled=True)
    else:
        text = input_data
    entities = extract_entities(text)
    return entities

st.title("TrustLevel NER Extractor")
st.text("Works for Articles (URL or Text) and Queries")

input_type = st.selectbox("Select input type:", ["URL", "Article Text", "User Query"])

if st.button('Load Example'):
    if input_type == "URL":
        st.session_state.input_data = "https://sputnikglobe.com/20231203/palestinian-leader-calls-on-icc-to-speed-up-israeli-war-crimes-trial--reports-1115353279.html"
    elif input_type == "Article Text":
        st.session_state.input_data = """Israel Shells Lebanon in Retaliatory Move – Statement
        09:20 GMT 04.12.2023 (Updated: 09:39 GMT 04.12.2023)
        © AFP 2023 / MENAHEM KAHANA
        Subscribe
        The Israel Defense Forces said in a statement that they had documented shelling from Lebanon towards IDF outpost and opened fire in response.
        “A number of mortar shell launches from Lebanon toward an IDF post in the area of Yiftah were identified. In response, IDF artillery struck the sources of the fire,” the Israeli army said on its official Telegram channel.
        Earlier, another round of shelling was documents, which resulted in three injured Israeli soldiers.
        “Three IDF soldiers were lightly injured and evacuated to receive medical treatment. Their families have been notified,” the statement read. The situation in South Lebanon heated up after Israel had its launched military operation in the Gaza Strip against Hamas. The Lebanese militant organization Hezbollah started shelling Israeli territory, with the IDF responding in kind.
        West Bank Death Toll From Israeli Fire Reaches 464 Since Early 2023 - Palestinian Ministry
        The death toll in the West Bank as a result of clashes with Israeli forces has reached 464 since the beginning of 2023, including 256 since October 7, the Palestinian Health Ministry said on Monday.
        "The death toll in the West Bank from Israeli army fire is 464 since the beginning of the year, including 256 since October 7," the ministry said in a statement.
        World
        Palestine-Israel conflict
        Israeli-Palestinian conflict
        Israel-Gaza conflict
        Israel Defense Forces (IDF)
        Gaza Strip
        Hamas
        Hezbollah
        Middle East
        Fresh and edgy: visit our channel on TikTok
        Follow
        """
    else:
        st.session_state.input_data = "israelian palestine conflict"

input_data = st.text_area("Enter data based on your selection above:", key="input_data")

if input_data:
    with st.spinner('Processing...'):
        entities = process_input(input_type, input_data)
    
        data = [(entity, ', '.join(values)) for entity, values in entities.items()]

        st.subheader("Named Entities")
        st.table(data)
        st.markdown("Description of entities can be found [here](https://stackoverflow.com/questions/76206507/spacy-where-are-terminologies-defined)")
