
import csv
import json
from concurrent.futures import ProcessPoolExecutor
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel
from scraper import scrape_article_text

from ner import get_entities_from_article_content


def blue_print(text: str) -> None:
    print(f"\033[94m{text}\033[0m")

load_dotenv()

class Article(BaseModel):
    title: str
    url: str
    scraped_content: Optional[str] = None
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
    article.scraped_content = scrape_article_text(article.url) 
    named_entities = get_entities_from_article_content(article.scraped_content)
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
            # Combining the queries for the current row
            combined_query = article_query + author_query + publisher_query
            
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
                'Scraped Content': article.scraped_content,
                'Date': article.isodate,
                'Author': article.author,
                'Publisher': article.publisher,
                'NamedEntities': article.named_entities
            })
        blue_print(f"Article {article.title} written to process input.")


    queries = generate_cypher_queries("data/processed_input.csv")

    # Write the queries to generated_cypher_queries.txt
    with open("data/generated_cypher_queries.cypherl", "w") as file:
        for query in queries:
            file.write(query + ";\n")


    from kg import execute_queries_from_file

    execute_queries_from_file("data/generated_cypher_queries.cypherl")


if __name__ == "__main__":
    main()
