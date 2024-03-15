from typing import List, Tuple

from neo4j import GraphDatabase
from pydantic import BaseModel
from streamlit_agraph import Edge, Node

from ner import NamedEntity


class Article(BaseModel):
    biasscore: float
    polarityscore: float
    trustlevel: float
    publicationdate: str
    title: str
    url: str
    mentioned_entities: List[str]


def fetch_articles_and_relations_for_entities(entities: List[NamedEntity], uri="bolt://localhost:7687", user="", password="") -> Tuple[List[Article], List[Node], List[Edge]]:
    driver = GraphDatabase.driver(uri, auth=(user, password))

    # Prepare node details for query
    where_conditions = []
    for entity in entities:
        where_conditions.append(f"(entity:{entity.type.capitalize()} AND entity.name = '{entity.text}')")

    where_conditions_query = " OR ".join(where_conditions)

    # Cypher query to fetch articles and their relations to entities
    query = f"""
    MATCH (article:Article)-[r:MENTIONS]->(entity)
    WHERE {where_conditions_query}
    RETURN article, r, entity
    """

    print(f"\n\n\n{query}\n\n\n")

    articles = []
    nodes = []
    edges = []
    processed_node_ids = set()

    with driver.session() as session:
        results = session.run(query)
        for record in results:
            article_node = record["article"]
            entity_node = record["entity"]
            relationship = record["r"]

            # Process article as a node
            if article_node.id not in processed_node_ids:
                nodes.append(Node(id=str(article_node.id),
                                  label=f"Article:{article_node.get('title', '')}\nTrustlevel:{article_node.get('trustlevel', '')}",
                                  size=30))
                processed_node_ids.add(article_node.id)
                articles.append(Article(**article_node, mentioned_entities=[entity_node.get('name')]))
            else:
                for article in articles:
                    if article.url == article_node.get('url'):
                        article.mentioned_entities.append(entity_node)
                        break
            # Process entity as a node
            if entity_node.id not in processed_node_ids:
                nodes.append(Node(id=str(entity_node.id),
                                  label=f"Entity:{entity_node.get('name', '')}",
                                  size=20))
                processed_node_ids.add(entity_node.id)

            # Process relationship as an edge
            edges.append(Edge(source=str(article_node.id),
                              label=relationship.type,
                              target=str(entity_node.id)))

    # Close the connection to the database
    driver.close()

    return articles, nodes, edges
