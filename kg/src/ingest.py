
import csv
import json
from concurrent.futures import ProcessPoolExecutor
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv("../.env")
load_dotenv(".env")
import time

from entity_recognition import NamedEntity, get_entities_from_text
from graphdb import execute_queries, execute_query
from logger import color_print
from nlp import clean_article_content
from pydantic import BaseModel
from scraper import scrape_article_text
from trustlevel import get_trustlevel_from_content


class RawArticle(BaseModel):
    title: str
    url: str
    content: Optional[str] = None
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
    return ProcessedArticle(**article.model_dump(), named_entities=named_entities)


def generate_cypher_queries(articles: List[ProcessedArticle]) -> List[str]:
    queries = []

    # with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    # reader = csv.DictReader(csvfile)
    # for row in reader:
    # Simplification: Assuming trustlevel, bias score, polarity score as default values
    # Adjust or enhance based on actual data availability or estimation logic
    for article in articles:

        trustlevel = -1
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
            f"MERGE (article:Article {{title: '{
                article.title.replace("'", "\\'")}', "
            f"publicationdate: '{article.isodate}', trustlevel: {
                trustlevel}, biasscore: {bias_score}, "
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

        entity_queries = ""
        merged_entities = set()  # Keep track of entities that have already been merged

        for entity in article.named_entities:
            entity_text_safe = entity.text.replace(
                "'", "\\'")  # Make entity safe for Cypher query
            # Unique key for each entity
            entity_key = f"{entity.type}:{entity.text}"

            if entity_key not in merged_entities:
                # Only generate MERGE statement if this entity hasn't been merged yet
                entity_queries += f"MERGE ({entity.type}_{entity_text_safe.replace(' ', '_').replace('-', '_')}:{entity.type.capitalize()} {{name: '{entity_text_safe}'}})\n"
                merged_entities.add(entity_key)

            # Use the entity variable for creating the relationship
            entity_queries += f"MERGE (article)-[:MENTIONS]->({entity.type}_{entity_text_safe.replace(' ', '_').replace('-', '_')})"

        # Combining the queries for the current row
        combined_query = article_query + author_query + publisher_query + entity_queries + ";"

        queries.append(combined_query)

    return queries


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
            processed_articles = list(executor.map(process_article, articles))
        # Write the processed articles to the file if it was not found or could not be opened
        with open("../data/processed_input.csv", "w", newline='') as output_file:
            fieldnames = ['Title', 'Url', 'Content',
                          'Date', 'Author', 'Publisher', 'NamedEntities']
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            for article in processed_articles:
                serialized_named_entities = json.dumps(
                    [ne.model_dump() for ne in article.named_entities], ensure_ascii=False)
                writer.writerow({
                    'Title': article.title,
                    'Url': article.url,
                    'Content': article.content,
                    'Date': article.isodate,
                    'Author': article.author,
                    'Publisher': article.publisher,
                    'NamedEntities': serialized_named_entities
                })

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
    # scraped_text = scrape_article_text("https://sputnikglobe.com/20231203/palestinian-leader-calls-on-icc-to-speed-up-israeli-war-crimes-trial--reports-1115353279.html")
    # article_title = "Palestinian Leader Calls on ICC to Speed Up Israeli War Crimes Trial"
    # curated_text = extract_article_content(article_title, scraped_text)
    # color_print(f"\nSCRAPED\n{scraped_text}")
    # color_print(f"\nCURATED\n{curated_text}")
