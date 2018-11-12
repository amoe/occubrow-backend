import pytest
from occubrow.backend import OccubrowBackend
from occubrow.neo4j_repository import RealNeo4jRepository

EXPECTED_DATA = {
    'directed': True,
    'graph': {},
    'links': [{'occurrences': 1, 'source': 0, 'target': 3, 'type': 'PRECEDES'},
              {'occurrences': 1, 'source': 0, 'target': 20, 'type': 'PRECEDES'},
              {'occurrences': 1, 'source': 1, 'target': 2, 'type': 'PRECEDES'},
              {'occurrences': 2, 'source': 2, 'target': 0, 'type': 'PRECEDES'},
              {'occurrences': 1, 'source': 20, 'target': 1, 'type': 'PRECEDES'}],
    'multigraph': False,
    'nodes': [{'content': 'foo', 'id': 0},
              {'content': 'baz', 'id': 1},
              {'content': 'quux', 'id': 2},
              {'content': 'fry', 'id': 3},
              {'content': 'bar', 'id': 20}]
}

phrases = [
    ["foo", "bar", "baz"],
    ["quux", "foo", "fry"],
    ["baz", "quux", "foo"]
]

# This functionality belongs in the repository, and shouldn't be directly in the
# backend, because it's only a smaller piece of the full transaction structure
# for adding a sentence.

def test_precedes_relationship(neo4j_driver):
    repository = RealNeo4jRepository(neo4j_driver)
    backend = OccubrowBackend(repository)

    for phrase in phrases:
        repository.add_precedes_links(phrase)

    assert backend.graph_matches(EXPECTED_DATA)
