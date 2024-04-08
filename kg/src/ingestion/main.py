
import csv
import json
from concurrent.futures import ProcessPoolExecutor
from typing import List

from dotenv import load_dotenv

load_dotenv("../.env")
load_dotenv(".env")

import time
import traceback

from entity_recognition import NamedEntity, get_entities_from_text
from graphdb import execute_queries, execute_query
from ingestion.graphdb import generate_cypher_queries
from ingestion.models import ProcessedArticle, RawArticle
from logger import color_print
from nlp import clean_article_content
from scraper import scrape_article_text
from tqdm import tqdm
from trustlevel import get_trustlevel_from_content


def blue_print(text: str) -> None:
    color_print(text, color='bue')


def load_articles_from_file(path: str) -> List[RawArticle]:
    articles = []
    with open(path, "r") as input_file:
        csv_reader = csv.DictReader(input_file)
        for row in csv_reader:
            article = RawArticle(
                title=row["Title"],
                url=row["Url"],
                content=row["Content"] if "Content" in row else None,
                isodate=row["Date"],
                author=row["Author"],
                publisher=row["Publisher"]
            )
            articles.append(article)
    return articles


def process_article(article: RawArticle) -> ProcessedArticle:
    color_print(f"Processing '{article.title}'.")
    if not article.content:
        scraped_content = scrape_article_text(article.url)
        article.content = clean_article_content(
            article_title=article.title, article_content=scraped_content)
    named_entities = get_entities_from_text(article.content)
    color_print(f"Article '{article.title}' processed.")
    trustlevel = None
    try:
        trustlevel = get_trustlevel_from_content(article.content)
    except Exception as e:
        color_print(f"Error on getting trustlevel for {article.title}: {str(e)}", color='red')
        
    if trustlevel is None:
        trustlevel = -1
    
    return ProcessedArticle(**article.model_dump(), named_entities=named_entities, trustlevel=trustlevel)



def process_articles(articles: List[RawArticle]) -> List[ProcessedArticle]:
    processed_articles = []
    color_print("Processing articles.", "green")
    try:
        with open("../data/processed_input.csv", "r", newline='') as input_file:
            color_print("Cached processed input found.", "green")
            reader = csv.DictReader(input_file)
            for row in reader:
                try:
                    named_entities = [NamedEntity(**e) for e in json.loads(row['NamedEntities'])]
                except Exception:
                    color_print(f"Could not read Named Entities of '{row['Title']}'", color="red")
                    continue

                processed_articles.append(ProcessedArticle(
                    title=row['Title'],
                    url=row['Url'],
                    content=row['Content'],
                    isodate=row['Date'],
                    author=row['Author'],
                    publisher=row['Publisher'],
                    trustlevel=row['Trustlevel'],
                    named_entities=named_entities)
                )
        if not processed_articles:  # If the file is empty, process articles
            color_print("Cached processed input not found.", "yellow")
            raise FileNotFoundError
        else:
            color_print("Using cached processed input.", "green")
    except (FileNotFoundError, IOError) as e:
        color_print(f"Could not read file. Error: {str(e)}")
        with ProcessPoolExecutor() as executor:
            processed_articles = list(tqdm(executor.map(process_article, articles), total=len(articles), desc="Processing Articles..."))
        # Write the processed articles to the file if it was not found or could not be opened
        with open("../data/processed_input.csv", "w", newline='') as output_file:
            fieldnames = ['Title', 'Url', 'Content',
                          'Date', 'Author', 'Publisher', 'NamedEntities', 'Trustlevel']
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            for article in processed_articles:
                try:
                    serialized_named_entities = json.dumps([ne.model_dump() for ne in article.named_entities], ensure_ascii=False)
                    writer.writerow({
                        'Title': article.title,
                        'Url': article.url,
                        'Content': article.content,
                        'Date': article.isodate,
                        'Author': article.author,
                        'Publisher': article.publisher,
                        'NamedEntities': serialized_named_entities,
                        'Trustlevel': article.trustlevel,
                    })
                except Exception as e:
                    color_print(f"Article '{article.title if article is not None else 'Unknown'}' failed to process! Error: {e}")
                    traceback.print_exc()
                    continue
    return processed_articles

def ingest():
    start_time = time.time()
    articles = load_articles_from_file("../data/input.csv")
    processed_articles = process_articles(articles)

    with open("../data/queries.txt", "a") as query_file:
        queries = generate_cypher_queries(processed_articles)
        query_file.write("\n".join(queries))

    execute_query("MATCH (n) DETACH DELETE n")
    execute_queries(queries)
    end_time = time.time()
    elapsed_time = end_time - start_time
    time_per_article = elapsed_time / len(processed_articles) if processed_articles else 0
    color_print(f"✅ Done! Processing Time: {elapsed_time:.2f} seconds", "green")
    color_print(f"{len(processed_articles)} Articles processed. Time per Article: {time_per_article:.2f} seconds", "green")


if __name__ == "__main__":
    ingest()