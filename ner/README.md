
# Project for exrtracting named entities out of articles (URLs or Text) & user queries

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
