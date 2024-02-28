
# TrustLevel NER Extractor

This is a PoC for creating a NER system to extract entities out of articles (both URL form or Text) as well as user queries to aid in further KG querying. 

### Demos

|     |     |     |
| --- | --- | --- |
| **Article URL** | **Article Text** | **User Query** |
| ![Article URL](/ner/assets/article_url.png) | ![Article Text](/ner/assets/article_text.png) | ![User Query](/ner/assets/user_query.png) |


## Setup

dependencies
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

spacy (ner)
```
python -m spacy download en_core_web_trf
```

playwright (web scraper)
```
playwright install chromium
```

env vars
```
cp .env.example .env
```

⚠️ Dont forget to change the env vars accordingly

## Running

```
streamlit run app.py
```
