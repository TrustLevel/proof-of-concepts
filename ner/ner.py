
import spacy


def extract_entities(text: str):
# Load English tokenizer, tagger, parser, NER, and word vectors
    nlp = spacy.load("en_core_web_trf")

    # Process the text
    doc = nlp(text)

    # Initialize a dictionary to store entities // List: https://stackoverflow.com/questions/76206507/spacy-where-are-terminologies-defined
    entities = {'PERSON': set([]), 'ORG': set([]), 'GPE': set([]), 'LOC': set( []), 'EVENT': set([])}

    # Extract entities
    for entity in doc.ents:
        if entity.label_ in entities:
            entities[entity.label_].add(entity.text)
    
    return entities