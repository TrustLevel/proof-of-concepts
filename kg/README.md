
# TrustLevel KG 

This is a PoC for creating the KG according to following diagram.

![KG System Architecture](/kg/assets/diagram.drawio.svg)


### Demos


|     |     |
| --- | --- |
| **KG Schema** | **Querying example** | 
| ![KG Schema](/kg/assets/kg_schema.png) | ![Querying Example](/kg/assets/querying_example.png) |




## Setup

### Memgraph
> [!WARNING]  
> You need to setup Memgraph DB. Head [here](https://memgraph.com/docs/getting-started) to get started. 

**Why Memgraph?**
- Neo4j cypher language compatibility
- 8x faster
- Easier to setup locally for prototyping


### Dependencies
```
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
``` 

### Playweight (scraper)
```
python -m playwright install chromium
```

### Env vars
```
cp .env.example .env
```
> [!WARNING]  
> Dont forget to change the env vars accordingly


## Running

### Graph DB

#### DB
```
docker run -d -p 7687:7687 --name memgraph memgraph/memgraph-mage
```

#### Local Memgraph Lab / GUI Explorer (optional)
```
docker run -d -p 3000:3000 --name memgraphlab memgraph/lab
```

Then navigate to http://lolcahost:3000


### Ingestion
```
cd src
python -m ingest
```
 
> [!TIP]  
> If you want to run with custom data, change `data/input.csv` while obbeying the present schema.



### Querying

```
streamlit run src/app.py
```