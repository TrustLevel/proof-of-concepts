from neo4j import GraphDatabase


# Function to execute queries from a file
def execute_queries_from_file(file_path, user="", password="", uri="bolt://localhost:7687"):
    # Connect to the database
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    # Open the file containing Cypher queries
    with open(file_path, 'r') as file:
        queries = file.read().split(';')  # Assuming queries are separated by semicolons
        
    # Execute each query in the file
    with driver.session() as session:
        for query in queries:
            query = query.strip()  # Remove leading/trailing whitespace
            if query:  # Check if query is not empty
                session.run(query)
                
                
    # Close the connection to the database
    driver.close()
