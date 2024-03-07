from typing import List, Literal

import spacy
from pydantic import BaseModel


class NamedEntity(BaseModel):
    type: Literal['location', 'organization', 'person', 'event']
    text: str

def get_entities_from_text(text: str) -> List[NamedEntity]:
    nlp = spacy.load("en_core_web_trf")

    doc = nlp(text)

    named_entities = []

    label_mapping = {
        'PERSON': 'person',
        'GPE': 'location',
        'LOC': 'location',
        'ORG': 'organization',
        'EVENT': 'event'
    }

    for entity in doc.ents:
        print(entity)
        print(entity.label_)
        if entity.label_ in label_mapping:
            named_entities.append(NamedEntity(type=label_mapping[entity.label_], text=entity.text))

    return named_entities


if __name__ == "__main__":
    print(get_entities_from_text("Palestine"))