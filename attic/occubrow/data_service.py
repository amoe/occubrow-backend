CREATE_PARENT_SENTENCE_STATEMENT = """
    CREATE (s1:Sentence {tokens: {token_seq}})
"""

MERGE_TOKEN_STATEMENT = """
   MERGE (t1:Token {content: {token_content}})
"""

CREATE_CONTAINS_RELATIONSHIP = """
    MATCH (s1:Sentence {tokens: {token_seq}}), (t1:Token {content: {token_content}})
    CREATE (s1)-[:CONTAINS {relationship_properties}]->(t1);
"""

CREATE_CATEGORY_RELATIONSHIP_STATEMENT = """
    MATCH (s1:Sentence {tokens: {token_seq}}), (t1:Taxon {name: {category}})
    CREATE (s1)-[:IN_CATEGORY]->(t1)
"""

import misc
import pprint

class DataService(object):
    def __init__(self):
        pass

    def create_occupation_description_from_tokens(self, token_seq, category):
        result = misc.run_some_query(
            CREATE_PARENT_SENTENCE_STATEMENT, {
                'token_seq': token_seq,
                'category': category
            }
        )

        for index, value in enumerate(token_seq):
            self.merge_token(value)
            self.create_sentence_relationship(token_seq, index, value)

        self.create_category_relationship(token_seq, category)
                
        return result

    def create_category_relationship(self, token_seq, category):
        misc.run_some_query(
            CREATE_CATEGORY_RELATIONSHIP_STATEMENT, {
                'token_seq': token_seq,
                'category': category
            }
        )

    def merge_token(self, value):
        misc.run_some_query(MERGE_TOKEN_STATEMENT, {'token_content': value})

    def create_sentence_relationship(self, token_seq, index, value):
        rel_properties = {'index': index}

        if index == 0:
            rel_properties['firstToken'] = True
        elif index == len(token_seq) - 1:
            rel_properties['lastToken'] = True

        misc.run_some_query(
            CREATE_CONTAINS_RELATIONSHIP,
            {
                'token_seq': token_seq,
                'relationship_properties': rel_properties,
                'token_content': value
            }
        )