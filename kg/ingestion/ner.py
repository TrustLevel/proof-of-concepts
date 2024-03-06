from typing import List, Literal

import spacy
from pydantic import BaseModel


class NamedEntity(BaseModel):
    type: Literal['location', 'organization', 'person', 'event']
    text: str

def get_entities_from_article_content(content: str) -> List[NamedEntity]:
    nlp = spacy.load("en_core_web_trf")

    doc = nlp(content)

    named_entities = []

    label_mapping = {
        'PERSON': 'person',
        'ORG': 'organization',
        'GPE': 'location',
        'LOC': 'location',
        'EVENT': 'event'
    }

    for entity in doc.ents:
        if entity.label_ in label_mapping:
            named_entities.append(NamedEntity(type=label_mapping[entity.label_], text=entity.text))

    return named_entities
