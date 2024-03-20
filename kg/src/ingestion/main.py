
import csv
import json
from concurrent.futures import ProcessPoolExecutor
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv("../.env")
load_dotenv(".env")

from pydantic import BaseModel

from entity_recognition import NamedEntity, get_entities_from_text
from graphdb import execute_queries, execute_query
from logger import color_print
from nlp import clean_article_content
from scraper import scrape_article_text
from trustlevel import get_trustlevel_from_content


def blue_print(text: str) -> None:
    color_print(text, color='bue')

class RawArticle(BaseModel):
    title: str
    url: str
    isodate: str
    author: str
    publisher: str


class ProcessedArticle(RawArticle):
    title: str
    url: str
    content: str 
    named_entities: List[NamedEntity]
    isodate: str
    author: str
    publisher: str


def load_articles_from_file(path: str) -> List[RawArticle]:
    articles = []
    with open(path, "r") as input_file:
        csv_reader = csv.DictReader(input_file)
        for row in csv_reader:
            article = RawArticle(
                title=row["Title"],
                url=row["Url"],
                isodate=row["Date"],
                author=row["Author"],
                publisher=row["Publisher"]
            )
            articles.append(article)
    return articles


def process_article(article: RawArticle) -> ProcessedArticle:
    blue_print(f"Processing '{article.title}'.")
    scraped_content = scrape_article_text(article.url) 
    clean_content = clean_article_content(article_title=article.title, scraped_text=scraped_content)
    named_entities = get_entities_from_text(article.content)
    blue_print(f"Article '{article.title}' processed.")
    return ProcessedArticle(**article, content=clean_content, named_entities=named_entities)


def generate_cypher_queries(articles: List[ProcessedArticle]) -> List[str]:
    queries = []
    
    # with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        # reader = csv.DictReader(csvfile)
        # for row in reader:
            # Simplification: Assuming trustlevel, bias score, polarity score as default values
            # Adjust or enhance based on actual data availability or estimation logic
    for article in articles:

        try:
            trustlevel = get_trustlevel_from_content(article.content)
            if trustlevel is None:
                trustlevel = -1
        except Exception as e:
            color_print(f"Error on getting trustlevel for {article.title}: {str(e)}", color='red')
            continue
        
        bias_score = trustlevel
        polarity_score = trustlevel
        
        article_query = (
            f"MERGE (article:Article {{title: '{article.title.replace("'", "\\'")}', "
            f"publicationdate: '{article.isodate}', trustlevel: {trustlevel}, biasscore: {bias_score}, "
            f"polarityscore: {polarity_score}, url: '{article.url}'}})\n"
        )
        
        author_query = (
            f"MERGE (author:Person {{name: '{article.author.replace("'", "\\'")}'}})\n"
            f"MERGE (author)-[:WRITES]->(article)\n"
        )
        
        publisher_query = (
            f"MERGE (publisher:Publisher {{name: '{article.publisher.replace("'", "\\'")}'}})\n"
            f"MERGE (publisher)-[:PUBLISHES]->(article)\n"
        )
        
        named_entities = json.loads(article.named_entities)
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
    try:
        with open("data/processed_input.csv", "r", newline='') as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                processed_articles.append(ProcessedArticle(title=row['Title'], url=row['Url'], content=row['Scraped Content'], isodate=row['Date'], author=row['Author'], publisher=row['Publisher'], named_entities=row['NamedEntities']))
        if not processed_articles:  # If the file is empty, process articles
            raise FileNotFoundError
    except (FileNotFoundError, IOError):
        with ProcessPoolExecutor() as executor:
            processed_articles = list(executor.map(process_article, articles))
        # Write the processed articles to the file if it was not found or could not be opened
        with open("data/processed_input.csv", "w", newline='') as output_file:
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
                    'NamedEntities': json.dumps(article.named_entities)  # Assuming named_entities needs to be serialized
                })

    queries = generate_cypher_queries(processed_articles)

    execute_query("MATCH (n) DETACH DELETE n")
    execute_queries(queries)


if __name__ == "__main__":
    main()
    # scraped_text = scrape_article_text("https://sputnikglobe.com/20231203/palestinian-leader-calls-on-icc-to-speed-up-israeli-war-crimes-trial--reports-1115353279.html")
    # article_title = "Palestinian Leader Calls on ICC to Speed Up Israeli War Crimes Trial"
    # curated_text = extract_article_content(article_title, scraped_text)
    # blue_print(f"\nSCRAPED\n{scraped_text}")
    # blue_print(f"\nCURATED\n{curated_text}")
