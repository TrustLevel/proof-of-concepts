from typing import List, Tuple

from neo4j import GraphDatabase
from streamlit_agraph import Edge, Node

from ner import NamedEntity


def fetch_articles_related_to_nodes(entities: List[NamedEntity], uri="bolt://localhost:7687", user="", password="") -> Tuple[List[Node], List[Edge]]:
    driver = GraphDatabase.driver(uri, auth=(user, password))

    # Prepare node details for query
    where_conditions = []
    for entity in entities:
        where_conditions.append(f"(n:{entity.type.capitalize()} AND n.name = '{entity.text}')")

    where_conditions_query = " OR ".join(where_conditions)

    # Cypher query to fetch articles which have a mention relationship to the given nodes
    query = f"""
    MATCH (article:Article)-[r:MENTIONS]->(n)
    WHERE {' OR '.join(where_conditions)}
    RETURN article, r, n
    """

    print(f"\n\n\n{query}\n\n\n")

    nodes = []
    edges = []
    processed_node_ids = set()

    with driver.session() as session:
        results = session.run(query)
        for record in results:
            # Extract node and article from record
            node, relationship, article = record["n"], record["r"], record["article"]

            # Process node
            if node.id not in processed_node_ids:
                nodes.append(Node(id=str(node.id),
                                  label=node.get("name", ""),
                                  size=25
                                  ))
                processed_node_ids.add(node.id)

            # Process article as end node
            if article.id not in processed_node_ids:
                nodes.append(Node(id=str(article.id),
                                  label=article.get("title", ""),
                                  size=25,
                                  ))
                processed_node_ids.add(article.id)

            # Process relationship
            edges.append(Edge(source=str(node.id),
                              label=relationship.type,
                              target=str(article.id)))
    # Close the connection to the database
    driver.close()

    return nodes, edges
