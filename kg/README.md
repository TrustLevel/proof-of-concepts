
# TrustLevel KG 

This is a PoC for creating the KG according to following diagram.

![KG System Architecture](/kg/assets/diagram.drawio.svg)


### Demos


|     |     |
| --- | --- |
| **KG Schema** | **Querying example** | 
| ![KG Schema](/kg/ingestion/assets/kg_schema.png) | ![Querying Example](/kg/querying/assets/querying_example.png) |




## Setup

dependencies
```
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
``` 

spacy (ner)
```
python -m spacy download en_core_web_trf
```

```
python -m playwright install chromium
```

env vars
```
cp .env.example .env
```

⚠️ Dont forget to change the env vars accordingly

## Running


### Ingestion
```
cd ingestion
python main.py
```
 
 💡 If you want to run with custom data, change `data/input.csv` while obbeying the present schema.



### Querying

<still buggy>

```
cd querying
streamlit run app.py
```