from typing import List, Optional, Tuple

from entity_recognition import NamedEntity
from neo4j import GraphDatabase
from neo4j.graph import Node
from pydantic import BaseModel
from streamlit_agraph import Edge, Node


class FetchedArticle(BaseModel):
    id: int
    biasscore: float
    polarityscore: float
    trustlevel: float
    publicationdate: str
    title: str
    url: str
    mentioned_entities: List[str]
    author: Optional[str] = None
    publisher: Optional[str] = None


def fetch_articles_and_relations_for_entities_authors_and_publishers(entities: List[NamedEntity], authors: List[str] = [], publishers: List[str] = [], uri="bolt://localhost:7687", user="", password="") -> Tuple[List[FetchedArticle], List[Node], List[Edge]]:
    driver = GraphDatabase.driver(uri, auth=(user, password))

    # Prepare node details for query
    entity_where_conditions = []
    for entity in entities:
        if entity.text not in authors and entity.text not in publishers:
            entity_where_conditions.append(f"(entity:{entity.type.capitalize()} AND entity.name = '{entity.text}')")
    
    query_parts = []
    return_parts = []
    if len(entity_where_conditions) > 0:
        query_parts.append("MATCH (article:Article)-[r1:MENTIONS]->(entity)")
        query_parts.append("WHERE " + " OR ".join(entity_where_conditions))
        return_parts.extend(['article', 'r1', 'entity'])
    if authors:
        query_parts.append("OPTIONAL MATCH (author: Person)-[r2:WRITES]->(article)")
        query_parts.append(f"WHERE author.name IN {authors}")
        return_parts.extend(['article', 'author', 'r1'])
    if publishers:
        query_parts.append("OPTIONAL MATCH (publisher: Publisher)-[r3:PUBLISHES]->(article)")
        query_parts.append(f"WHERE publisher.name IN {publishers}")
        return_parts.extend(['article', 'publisher', 'r3'])
    query_parts.append("RETURN " + ", ".join(list(set(return_parts))))
    query = "\n".join(query_parts)

    print(f"\n\n\n{query}\n\n\n")

    articles = []
    nodes = []
    edges = []
    processed_node_ids = set()

    with driver.session() as session:
        results = session.run(query)
        records = list(results)

    driver.close()

    for record in records:
        article_node = record.get("article")
        # Initialize an empty list to collect mentioned entities for each article
        if article_node.id not in processed_node_ids:
            mentioned_entities = []
            nodes.append(Node(id=str(article_node.id),
                                label=f"Article:{article_node.get('title', '')}",
                                size=30))
            processed_node_ids.add(article_node.id)
            articles.append(FetchedArticle(**article_node, id=article_node.id, mentioned_entities=mentioned_entities))
        
    for record in records:
        # Iterate over all possible nodes (entities, authors, publishers) and their relationships
        for node_key in record.keys():
            if node_key not in ["article", "r1", "r2", "r3"]:
                mentioned_node = record.get(node_key)
                if mentioned_node and mentioned_node.id not in processed_node_ids:
                    # Determine label based on node type (use 'name' or 'title' as appropriate)
                    node_label = mentioned_node.get('name', mentioned_node.get('title', ''))
                    node_type = list(mentioned_node.labels)[0]  # Assuming the first label is the type
                    nodes.append(Node(id=str(mentioned_node.id),
                                        label=f"{node_type}:{node_label}",
                                        size=20))
                    processed_node_ids.add(mentioned_node.id)
                            

        # Process relationships as edges and add entities, publishers, or authors to the respective article
        for rel_key in ["r1", "r2", "r3"]:
            relationship = record.get(rel_key)
            if relationship is not None:
                source_node, target_node = relationship.nodes
                node_ids = [n.id for n in nodes]
                # Check if both nodes are present in the current graph
                if source_node.element_id in node_ids and target_node.element_id in node_ids:
                    edges.append(Edge(source=str(source_node.element_id),
                                      label=relationship.type,
                                      target=str(target_node.element_id)))
                    # Depending on the relationship type, add the entity to the respective article's mentioned_entities list
                    if relationship.type == "MENTIONS":
                        for article in articles:
                            if str(article.id) == source_node.element_id:
                                article.mentioned_entities.append(target_node._properties.get('name'))
                    elif relationship.type == "WRITES":
                        for article in articles:
                            if str(article.id) == target_node.element_id:
                                article.authors.append(source_node._properties.get('name'))
                    elif relationship.type == "PUBLISHES":
                        for article in articles:
                            if str(article.id) == target_node.element_id:
                                article.publisher = str(source_node._properties.get('name'))


    return articles, nodes, edges


def execute_query(query_str, user="", password="", uri="bolt://localhost:7687"):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    with driver.session() as session:
        session.run(query_str.strip())
        
    driver.close()

def execute_queries(queries: List[str], user="", password="", uri="bolt://localhost:7687"):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    with driver.session() as session:
        for query in queries:
            query = query.strip()  
            if query:  
                session.run(query)
        
    driver.close()

def execute_queries_from_file(file_path, user="", password="", uri="bolt://localhost:7687"):
    with open(file_path, 'r') as file:
        queries = file.read().split(';') 
        
    return execute_queries(queries, user=user, password=password, uri=uri)
