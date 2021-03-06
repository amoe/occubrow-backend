import pytest
import copy
import networkx
from occubrow.backend import OccubrowBackend, strict_eq
from occubrow.test_utility import make_backend, tree_matches
from occubrow.neo4j_repository import RealNeo4jRepository

# functional test, note that this shows that we actually don't have a 1 to 1
# translation between these formats which is probably not the best, perhaps
# we should mandate the 'content' format for input as well?

EXPECTED_EXPORT_DATA = {
    'children': [{'content': 'Rock', 'id': 1, 'label': 'Taxon'},
                 {'content': 'Classical', 'id': 2, 'label': 'Taxon'}],
    'content': 'Music',
    'id': 0,
    'label': 'Taxon'
}

input_data = {
    'id': 'Music',
    'children': [
        {
            'id': 'Rock',
            'children': []
        },
        {
            'id': 'Classical',
            'children': []
        }
    ]
}

# We can't just parse to a tree because children can be in an arbitrary order.

@pytest.mark.functional
def test_can_export_taxonomy_tree(neo4j_driver):
    backend = make_backend(RealNeo4jRepository(neo4j_driver))
    backend.import_taxonomy(input_data)
    root = 'Music'
    tree_data = backend.export_taxonomy_tree(root)
    assert tree_matches(tree_data, EXPECTED_EXPORT_DATA)
    


