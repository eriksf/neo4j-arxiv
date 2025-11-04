import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from db import Neo4jConnection

load_dotenv()

NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_CONNECTION_URI = os.getenv("NEO4J_CONNECTION_URI")

conn = Neo4jConnection(uri=NEO4J_CONNECTION_URI, user=NEO4J_USERNAME, pwd=NEO4J_PASSWORD)

console = Console()

query_string_categories = '''
MATCH (c:Category)
RETURN c.category, COUNT { ()-[:IN_CATEGORY]->(c) } AS inDegree
ORDER BY inDegree DESC LIMIT 25
'''

result = conn.query(query_string_categories)
df = pd.DataFrame([dict(_) for _ in result])

# save image
plt.figure(figsize=(12,8))
ax = sns.barplot(x=df['c.category'], y=df['inDegree'])
ax.set_title('Top 25 Categories')
plt.xlabel('Category Name', fontsize=18)
plt.ylabel('inDegree',fontsize=18)
plt.xticks(rotation='vertical', fontsize=18)
plt.savefig("categories.png", bbox_inches="tight")

# print table
table = Table(title="Top 25 Categories")
table.add_column("Category")
table.add_column("inDegree")
for record in result:
    table.add_row(record[0], str(record[1]))
console.print(table)
print("\n")

query_string_authored = '''
MATCH (a:Author)-[:AUTHORED]->(p:Paper)
RETURN a.name AS author, count(p) AS numberOfPapers
ORDER BY numberOfPapers DESC LIMIT 25
'''

result = conn.query(query_string_authored)
df = pd.DataFrame([dict(_) for _ in result])

# save image
plt.figure(figsize=(12,8))
ax = sns.barplot(x=df['author'], y=df['numberOfPapers'])
ax.set_title('Top 25 Authors')
plt.xlabel('Author', fontsize=18)
plt.ylabel('Papers',fontsize=18)
plt.xticks(rotation='vertical', fontsize=18)
plt.savefig("authors.png", bbox_inches="tight")

# print table
table = Table(title="Top 25 Authors")
table.add_column("Author")
table.add_column("Papers")
for record in result:
    table.add_row(record[0], str(record[1]))
console.print(table)

