
# Project for augmenting TrustLevel KG `input.csv` with entities

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

playwright (scraper)
```
playwright install chromium
```


## Running

```
streamlit run app.py
```
