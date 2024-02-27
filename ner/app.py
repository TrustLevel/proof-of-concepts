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
    elif input_type == 'User Query':
        text = rewrite_query(input_data)
        st.text_area("Rewritten Query (optimized for entity extraction):", value=text, height=100, disabled=True)
    else:
        text = input_data
    entities = extract_entities(text)
    return entities

st.title("Content Processor")

input_type = st.selectbox("Select input type:", ["URL", "Article Text", "User Query"])

if st.button('Load Example'):
    if input_type == "URL":
        st.session_state.input_data = "https://sputnikglobe.com/20231203/palestinian-leader-calls-on-icc-to-speed-up-israeli-war-crimes-trial--reports-1115353279.html"
    elif input_type == "Article Text":
        st.session_state.input_data = """Palestinian Leader Calls on ICC to Speed Up Israeli War Crimes Trial – Reports
        10:01 GMT 03.12.2023 (Updated: 09:24 GMT 05.12.2023)
        Israeli Military Struck Hamas Facilities in Gaza Strip – Statement
        The Israel Defense Forces (IDF) said on Sunday it had struck at infrastructure and weapons storage facilities of Palestinian group Hamas in the Gaza Strip, eliminating five fighters of the movement. The Israeli naval troops also struck at Hamas targets over the past 24 hours, the statement read. On October 7, Hamas launched a large-scale rocket attack against Israel from the Gaza Strip and breached the border. Israel launched retaliatory strikes and ordered a complete blockade of Gaza, cutting off supplies of water, food, and fuel. On October 27, Israel launched a ground incursion into the Gaza Strip with the declared goal of eliminating Hamas fighters and rescuing the hostages.
        Last week, Qatar mediated a deal between Israel and Hamas on a temporary truce and the exchange of some of the prisoners and hostages, as well as the delivery of humanitarian aid into the Gaza Strip. The truce was extended several times, but on Friday, December 1, the Israeli military resumed fighting against Hamas in the Gaza Strip, saying the group had violated the humanitarian pause by opening fire on Israeli territory.
        Israeli Airstrikes on Refugee Camp in Gaza Claim Lives of 14 People – Reports
        At least 14 people, including children and women, were killed in the Israeli airstrikes on the Nuseirat refugee camp in the central Gaza Strip, Palestinian news agency reported on Sunday. The death toll is expected to increase as rescue operations continue, the report added.
        Shia Muslim Militant Groups Attacked US Base in Iraqi Kurdistan - Statement
        The Islamic Resistance in Iraq, which includes Shia Muslim militant groups, said on Saturday that it had carried out a drone attack on a US base at Erbil Airport in Iraqi Kurdistan. "In response to the crimes the enemy is committing against our people in Gaza, Iraqi Islamic Resistance fighters used a drone to attack the US occupation base at Erbil Airport," the group said in a statement. On Thursday, Pentagon Deputy Press Secretary Sabrina Singh said that US forces in Iraq and Syria had been attacked 74 times since October.
        """
    else:
        st.session_state.input_data = "israelian palestine conflict"

input_data = st.text_area("Enter data based on your selection above:", key="input_data")

if input_data:
    with st.spinner('Processing...'):
        entities = process_input(input_type, input_data)
    
        data = [(entity, ', '.join(values)) for entity, values in entities.items()]
    
        st.table(data)
