from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None

        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response
    
    def insert(self, query, parameters=None, db=None, max_retries=3):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            total_inserted = session.execute_write(self._create_transaction, query, parameters)
            print(f"{total_inserted} nodes inserted")
        except Exception as e:
            print("Insert failed:", e)
        finally:
            if session is not None:
                session.close()

    @staticmethod
    def _create_transaction(tx, query, parameters):
        result = tx.run(query, parameters)
        record = result.single()
        return record['total']


def add_categories(conn, categories):
    # Adds category nodes to the Neo4j graph.
  
    query = '''UNWIND $rows AS row
    MERGE (c:Category {category: row.category})
    RETURN count(*) as total
    '''
    
    conn.insert(query, parameters={'rows': categories.to_dict('records')})


def add_authors(conn, rows):
    # Adds author nodes to the Neo4j graph as a batch job.

    query = '''UNWIND $rows AS row
               MERGE (:Author {name: row.author})
               RETURN count(*) as total
    '''

    conn.insert(query, parameters={'rows': rows.to_dict('records')})


def add_papers(conn, rows):
    # Adds paper nodes and (:Author)--(:Paper) and (:Paper)--(:Category)
    # relationships to the Neo4j graph as a batch job.  (Note the smaller batch
    # size due to the fact that this function is adding much more data than the
    # add_authors() function.)

    query = '''
    UNWIND $rows as row
    MERGE (p:Paper {id:row.id}) ON CREATE SET p.title = row.title

    // connect categories
    WITH row, p
    UNWIND row.category_list AS category_name
    MATCH (c:Category {category: category_name})
    MERGE (p)-[:IN_CATEGORY]->(c)

    // connect authors
    WITH distinct row, p // reduce cardinality
    UNWIND row.cleaned_authors_list AS author
    MATCH (a:Author {name: author})
    MERGE (a)-[:AUTHORED]->(p)
    RETURN count(distinct p) as total
    '''

    conn.insert(query, parameters={'rows': rows.to_dict('records')})
