from neo4j import GraphDatabase
# Connect to the Neo4j database
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Billa@12"

def connectDatabase():
    try:
        with GraphDatabase.driver(uri, auth=(username, password)) as driver:
            # Start a session
            with driver.session() as session:
                # Run a simple query to check if the connection is successful
                result = session.run("RETURN 1")
                print("Connected to Neo4j Database!")

    except Exception as e:
        print(f"Error connecting to Neo4j Database: {e}")