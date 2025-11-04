import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
print(f"Username: '{NEO4J_USERNAME}'")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
print(f"Password: '{NEO4J_PASSWORD}'")
NEO4J_CONNECTION_URI = os.getenv("NEO4J_CONNECTION_URI")
print(f"Connect: '{NEO4J_CONNECTION_URI}'")

driver = GraphDatabase.driver(NEO4J_CONNECTION_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

try:
    driver.verify_connectivity()
    print("Connection successful!")

    with driver.session() as session:
        result = session.run("MATCH (n) RETURN COUNT(n) AS node_count")
        count = result.single()["node_count"]
        print(f"Number of nodes in the database: {count}")
except Exception as e:
    print(f"Failed to to connect to Neo4j: {e}")

