
import csv
import json
from concurrent.futures import ProcessPoolExecutor
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv("../.env")
load_dotenv(".env")

from nlp import extract_article_content
from pydantic import BaseModel
from scraper import scrape_article_text

from ner import get_entities_from_article_content


def blue_print(text: str) -> None:
    print(f"\033[94m{text}\033[0m")


class Article(BaseModel):
    title: str
    url: str
    content: Optional[str] = None
    named_entities: Optional[dict] = {}
    isodate: str
    author: str
    publisher: str


def load_articles_from_file(path: str) -> List[Article]:
    articles = []
    with open(path, "r") as input_file:
        csv_reader = csv.DictReader(input_file)
        for row in csv_reader:
            article = Article(
                title=row["Title"],
                url=row["Url"],
                isodate=row["Date"],
                author=row["Author"],
                publisher=row["Publisher"]
            )
            articles.append(article)
    return articles


def process_article(article):
    blue_print(f"Processing '{article.title}'.")
    scraped_content = scrape_article_text(article.url) 
    article.content = extract_article_content(article_title=article.title, scraped_text=scraped_content)
    named_entities = get_entities_from_article_content(article.content)
    entity_dict = {}
    for entity in named_entities:
        if entity.type not in entity_dict:
            entity_dict[entity.type] = []
        entity_dict[entity.type].append(entity.text)
    article.named_entities = json.dumps(entity_dict)  
    blue_print(f"Article '{article.title}' processed.")
    return article

import csv


def generate_cypher_queries(csv_file_path):
    queries = []
    
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Simplification: Assuming trustlevel, bias score, polarity score as default values
            # Adjust or enhance based on actual data availability or estimation logic
            trustlevel, bias_score, polarity_score = 0.5, 0.0, 0.0
            
            article_query = (
                f"MERGE (article:Article {{title: '{row['Title'].replace("'", "\\'")}', "
                f"publicationdate: '{row['Date']}', trustlevel: {trustlevel}, biasscore: {bias_score}, "
                f"polarityscore: {polarity_score}}})\n"
            )
            
            author_query = (
                f"MERGE (author:Person {{name: '{row['Author'].replace("'", "\\'")}'}})\n"
                f"MERGE (author)-[:WRITES]->(article)\n"
            )
            
            publisher_query = (
                f"MERGE (publisher:Publisher {{name: '{row['Publisher'].replace("'", "\\'")}'}})\n"
                f"MERGE (publisher)-[:PUBLISHES]->(article)\n"
            )
            
            named_entities = json.loads(row['NamedEntities'])
            entity_queries = ""
            merged_entities = set()  # Keep track of entities that have already been merged

            for entity_type, entities in named_entities.items():
                for entity in entities:
                    entity_safe = entity.replace("'", "\\'")  # Make entity safe for Cypher query
                    entity_key = f"{entity_type}:{entity_safe}"  # Unique key for each entity
                    
                    if entity_key not in merged_entities:
                        # Only generate MERGE statement if this entity hasn't been merged yet
                        entity_queries += f"MERGE ({entity_type}_{entity_safe.replace(' ', '_').replace('-', '_')}:{entity_type.capitalize()} {{name: '{entity_safe}'}})\n"
                        merged_entities.add(entity_key)
                    
                    # Use the entity variable for creating the relationship
                    entity_queries += f"MERGE (article)-[:MENTIONS]->({entity_type}_{entity_safe.replace(' ', '_').replace('-', '_')})\n"

            # Combining the queries for the current row
            combined_query = article_query + author_query + publisher_query + entity_queries
            
            queries.append(combined_query)
    
    return queries

def main():
    articles = load_articles_from_file("data/input.csv")
    processed_articles = []
    with ProcessPoolExecutor() as executor:
        processed_articles = list(executor.map(process_article, articles))
    
    with open("data/processed_input.csv", "w", newline='') as output_file:
        blue_print("Processed input reset.")
        fieldnames = ['Title', 'Url', 'Scraped Content', 'Date', 'Author', 'Publisher', 'NamedEntities']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for article in processed_articles:
            writer.writerow({
                'Title': article.title,
                'Url': article.url,
                'Scraped Content': article.content,
                'Date': article.isodate,
                'Author': article.author,
                'Publisher': article.publisher,
                'NamedEntities': article.named_entities
            })
        blue_print(f"Article {article.title} written to process input.")


    queries = generate_cypher_queries("data/processed_input.csv")

    # Write the queries to generated_cypher_queries.txt
    with open("queries/create_graph_content.cypherl", "w") as file:
        for query in queries:
            file.write(query + ";\n")


    from kg import execute_queries_from_file

    execute_queries_from_file("queries/wipe_graph.cypherl")
    execute_queries_from_file("queries/create_graph_content.cypherl")


if __name__ == "__main__":
    main()
    # scraped_text = scrape_article_text("https://sputnikglobe.com/20231203/palestinian-leader-calls-on-icc-to-speed-up-israeli-war-crimes-trial--reports-1115353279.html")
    # article_title = "Palestinian Leader Calls on ICC to Speed Up Israeli War Crimes Trial"
    # curated_text = extract_article_content(article_title, scraped_text)
    # blue_print(f"\nSCRAPED\n{scraped_text}")
    # blue_print(f"\nCURATED\n{curated_text}")
