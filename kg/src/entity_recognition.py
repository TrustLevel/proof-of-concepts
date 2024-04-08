from typing import List, Tuple

from gliner import GLiNER
from pydantic import BaseModel, field_validator
import warnings

warnings.filterwarnings("ignore", message="The sentencepiece tokenizer that you are converting to a fast tokenizer uses the byte fallback option which is not implemented in the fast tokenizers.*", category=UserWarning, module='transformers.convert_slow_tokenizer')

possible_entities = ['location', 'organization', 'person', 'event']

class NamedEntity(BaseModel):
    type: str
    text: str

    @field_validator('type')
    @classmethod
    def must_be_possible_entity(cls, v: str) -> str:
        if v not in possible_entities:
            raise ValueError(f'Entity type must be one of the following: {possible_entities}')
        return v
    
    def __hash__(self):
        return hash((self.type, self.text))

def get_authors_and_publishers_from_text(text: str) -> Tuple[List[str], List[str]]:

    labels = ['Article_Author', 'Media_Publisher']

    model = GLiNER.from_pretrained("urchade/gliner_base")
    entities = model.predict_entities(text, labels, threshold=0.5)

    authors = [e['text'] for e in entities if e['label'] == "Article_Author"]
    publishers = [e['text'] for e in entities if e['label'] == "Media_Publisher"]

    return authors, publishers


def get_entities_from_text(text: str) -> List[NamedEntity]:

    model = GLiNER.from_pretrained("urchade/gliner_base")
    entities = model.predict_entities(text, possible_entities, threshold=0.5)

    return set([NamedEntity(type=entity['label'], text=entity['text']) for entity in entities])

    # nlp = spacy.load("en_core_web_trf")

    # doc = nlp(text)

    # named_entities = []

    # label_mapping = {
    #     'PERSON': 'person',
    #     'ORG': 'organization',
    #     'GPE': 'location',
    #     'LOC': 'location',
    #     'EVENT': 'event'
    # }

    # for entity in doc.ents:
    #     if entity.label_ in label_mapping:
    #         named_entities.append(NamedEntity(type=label_mapping[entity.label_], text=entity.text))

    # return named_entities


if __name__ == "__main__":
    text = """"Israel’s deadly bombardment of Gaza has killed nearly 15,000 people, including 10,000 women and children, in over 50 days, making it the deadliest war for the besieged Palestinian enclave till date.

Israel has rebuffed calls for a ceasefire as a four-day humanitarian truce comes to an end on November 28. It is unclear whether the truce will be extended.

The devastation of Gaza and the mounting death toll has triggered worldwide protests, bringing the decades-long issue to the centre-stage of global politics.

The Balfour declaration

The Israeli-Palestinian issue goes back nearly a century when Britain, during World War I, pledged to establish a national home for the Jewish people in Palestine under the Balfour Declaration. British troops took control of the territory from the Ottoman Empire at the end of October 1917.

Jewish immigration to Palestine

A large-scale Jewish migration to Palestine began, accelerated by Jewish people fleeing Nazism in Europe. Between 1918 and 1947, the Jewish population in Palestine increased from 6 percent to 33 percent.

Palestinians were alarmed by the demographic change and tensions rose, leading to the Palestinian revolt from 1936 to 1939.

Meanwhile, Zionist organisations continued to campaign for a homeland for Jews in Palestine. Armed Zionist militias started to attack the Palestinian people, forcing them to flee. Zionism, which emerged as a political ideology in the late 19th century, called for the creation of a Jewish homeland.

The UN Partition Plan

As violence ravaged Palestine, the matter was referred to the newly formed United Nations. In 1947, the UN adopted Resolution 181, which called for the partition of Palestine into Arab and Jewish states, handing over about 55 percent of the land to Jews. Arabs were granted 45 percent of the land, while Jerusalem was declared a separate internationalised territory.

The city is currently divided between West Jerusalem, which is predominantly Jewish, and East Jerusalem with a majority Palestinian population. Israel captured East Jerusalem after the Six-Day War in 1967 along with the West Bank – a step not recognised by the international community.

The Old City in occupied East Jerusalem holds religious significance for Christians, Muslims, and Jews. It is home to Al-Aqsa Mosque compound, which is known to Muslims as al-Haram al-Sharif and to Jews as Temple Mount.

In 1981, the UN designated it a World Heritage Site.

The Nakba

Leading up to Israel’s birth in 1948, more than 750,000 Palestinians were ethnically cleansed from their homes by Zionist militias. This mass exodus came to be known as the Nakba or catastrophe.

A further 300,000 Palestinians were displaced by the Six-Day War in 1967.

Israel declared the annexation of East Jerusalem in 1980, but the international community still considers it an occupied territory. Palestinians want East Jerusalem as the capital of their future state.

The Oslo Accords

In 1993, Palestinian leader Yasser Arafat and Israeli Prime Minister Yitzhak Rabin signed the Oslo Accords, which aimed to achieve peace within five years. It was the first time the two sides recognised each other.

A second agreement in 1995 divided the occupied West Bank into three parts – Area A, B and C. The Palestinian Authority, which was created in the wake of the Oslo Accords, was offered only limited rule on 18 percent of the land as Israel effectively continued to control the West Bank.

Israeli settlements and checkpoints

However, the Oslo Accords slowly broke down as Israeli settlements, Jewish communities built on Palestinian land in the West Bank, grew at a rapid pace.

The settlement population in the West Bank and East Jerusalem grew from approximately 250,000 in 1993 to up to 700,000 in September this year. About three million Palestinians live in the occupied West Bank and East Jerusalem.

The building of Israeli settlements and a separation wall on occupied territories has fragmented the the Palestinian communities and restricted their mobility. About 700 road obstacles, including 140 checkpoints, dot the West Bank. About 70,000 Palestinians with Israeli work permits cross these checkpoints in their daily commute.

Settlements are considered illegal under international law. The UN has condemned settlements, calling it a big hurdle in the realisation of a viable Palestinian state as part of the so-called “two-state solution”.

Blockade of Gaza

Israel imposed a blockade on Gaza in 2007 after the Hamas group came to power. The siege continues till date. Israel also occupies the West Bank and East Jerusalem – the territories Palestinians want to be part of their future state.

Israel imposed a total blockade on the Gaza Strip on October 9, cutting its supplies of electricity, food, water, and fuel in the wake of a surprise Hamas attack inside Israel. At least 1,200 people were killed in that attack.

Israel and Palestine now

This is what Israel and Palestine look like now.

Today, about 5 million Palestinians live in Gaza, the West Bank and East Jerusalem and 1.6 million Palestinians are citizens of Israel. This makes up about half of their total population. The other half lives in other countries, including Arab countries. There are about 14.7 million Jews around the world today, of which 84 percent live in Israel and the United States. The rest live in other countries including France, Canada, Argentina and Russia.

Here is an account of Palestinian and Israeli lives lost to the violence between 2008 and 2023."
"""
    print(get_entities_from_text(text))