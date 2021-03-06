import neo4j
import occubrow.types
import occubrow.queries
from logging import debug
import uuid
import pdb
import occubrow.shim_graph

UPDATE_QUERY = """
    MATCH (t1:Token {content: $content1})-[r:PRECEDES]-(t2:Token {content: $content2})
    SET r.occurrences = r.occurrences + 1;
"""

INSERT_QUERY = """
    MATCH (t1:Token {content: $content1}), (t2:Token {content: $content2})
    CREATE (t1)-[:PRECEDES {occurrences: 1}]->(t2)
"""

MERGE_NODE_QUERY = """
    MERGE (t:Token {content: $content})
"""


def merge_node(session, content):
    session.run(MERGE_NODE_QUERY, content=content)

def create_or_increment_precedes_relationship(session, start_node, end_node):
    with session.begin_transaction() as tx:
        result = tx.run(UPDATE_QUERY, content1=start_node, content2=end_node)
        property_set_count = result.summary().counters.properties_set
        print("Property set count = %d" % property_set_count)
        
        if property_set_count == 0:
            tx.run(INSERT_QUERY, content1=start_node, content2=end_node)

class RealNeo4jRepository(object):
    def __init__(self):
        self.driver = neo4j.GraphDatabase.driver(uri="bolt://localhost:7687")

    def __init__(self, driver):
        self.driver = driver

    def pull_graph(self, canned_statement):
        results = self.run_canned_statement(canned_statement)
        row = results.single()

        # no rows were returned, the graph is empty.  the calling code can choose
        # to handle this case specially
        if row is None:
            return {'nodes': [], 'rels': []}

        return occubrow.shim_graph.shim_subgraph_result(row)

    # wrapper to allow asserting calls on this type
    def run_statement(self, statement, parameters=None, **kwparameters):
        with self.driver.session() as session:
            result = session.run(statement, parameters, **kwparameters)

        return result

    # run a specially typed query
    def run_canned_statement(self, canned_statement):
        with self.driver.session() as session:
            query = canned_statement.get_cypher()
            parameters = canned_statement.get_parameters()
            result = session.run(query, parameters)
            
        return result

    def add_precedes_links(self, phrase):
        """
        Add only the precedes links for one sentence.  This will only add a part
        of the database structure for a given sentence.  Phrase should be
        a tokenized list.
        """
        first_idx = 0
        last_idx = len(phrase) - 1

        for index in range(last_idx):
            start_node = phrase[index]
            end_node = phrase[index + 1]

            self._merge_sentence_links(start_node, end_node)

    def _merge_sentence_links(self, start_node, end_node):
        debug("Relationship: %s -> %s", start_node, end_node)

        with self.driver.session() as session:
            merge_node(session, start_node)
            merge_node(session, end_node)
            create_or_increment_precedes_relationship(session, start_node, end_node)   
