
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from ingestion.models import ProcessedArticle
from logger import color_print
from tqdm import tqdm
from trustlevel import get_trustlevel_from_content


def adapt_for_memgraph(s: str):
    adapted_str = re.sub(r'\W+', '_', s)
    adapted_str = adapted_str.strip('_')
    return adapted_str

def generate_cypher_query(article: ProcessedArticle) -> str:

    trustlevel = article.trustlevel
    bias_score = trustlevel
    polarity_score = trustlevel

    article_query = (
        f"MERGE (article:Article {{title: '{article.title.replace("'", "\\'")}', "
        f"publicationdate: '{article.isodate}', trustlevel: {trustlevel}, biasscore: {bias_score}, "
        f"polarityscore: {polarity_score}, url: '{article.url}'}})\n"
    )

    author_query = (
        f"MERGE (author:Person {{name: '{article.author}'}})\n"
        f"MERGE (author)-[:WRITES]->(article)\n"
    )

    publisher_query = (
        f"MERGE (publisher:Publisher {{name: '{article.publisher.replace("'", "\\'")}'}})\n"
        f"MERGE (publisher)-[:PUBLISHES]->(article)\n"
    )

    entity_queries = ""
    merged_entities = set()  # Keep track of entities that have already been merged

    for entity in article.named_entities:
        entity_text_safe = adapt_for_memgraph(entity.text)
        entity_key = f"{entity.type}:{entity.text}"

        if entity_key not in merged_entities:
            entity_queries += f"MERGE ({entity.type}_{entity_text_safe}:{entity.type.capitalize()} {{name: '{entity.text}'}})\n"
            merged_entities.add(entity_key)

        entity_queries += f"MERGE (article)-[:MENTIONS]->({entity.type}_{entity_text_safe})"

    combined_query = article_query + author_query + publisher_query + entity_queries + ";"
    return combined_query

def generate_cypher_queries(articles: List[ProcessedArticle]) -> List[str]:
    queries = []
    with ThreadPoolExecutor() as executor:
        # Wrap executor.map with tqdm for progress tracking
        futures = {executor.submit(generate_cypher_query, article): article for article in articles}
        for future in tqdm(as_completed(futures), total=len(articles), desc="Generating cypher queries..."):
            query = future.result()
            if query:
                queries.append(query)
    return queries