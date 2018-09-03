import networkx
import pprint
import json
import pytest
from logging import debug
import os
import subprocess
import yaml

import occubrow.neo4j_repository
import occubrow.neo4j_test_utility

EXPECTED_TAXONOMY_RESULT = {'_type': 'Taxon',
 'children': [{'_type': 'Taxon',
                'children': [{'_type': 'Taxon',
                               'id': 20717,
                               'name': 'Aurelia labiata'},
                              {'_type': 'Taxon',
                               'id': 20718,
                               'name': 'Aurelia aurita'}],
                'id': 20715,
                'name': 'Aurelia'},
               {'_type': 'Taxon',
                'children': [{'_type': 'Taxon',
                               'id': 20720,
                               'name': 'Deepstaria reticulum'},
                              {'_type': 'Taxon',
                               'id': 20719,
                               'name': 'Deepstaria enigmatica'}],
                'id': 20716,
                'name': 'Deepstaria'}],
 'id': 20714,
 'name': 'Ulmaridae'}

def get_repo_toplevel():
    output = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])
    return output.rstrip().decode('utf-8')

DEFAULT_ENVIRONMENT = 'default'

def get_environment():
    env = os.environ.get('OCCUBROW_ENVIRONMENT', DEFAULT_ENVIRONMENT)
    debug("using environment %s", env)

    config_path = os.path.join(get_repo_toplevel(), 'environments', "%s.yml" % env)

    with open(config_path, 'r') as f:
        data = yaml.load(f, Loader=yaml.Loader)

    return data

def get_neo4j_port():
    return get_environment()['neo4j_port']

@pytest.fixture(scope='function')
def neo4j():
    debug("setting up neo4j")
    obj = occubrow.neo4j_repository.Neo4jRepository(port=get_neo4j_port())
    obj.clear_all()
    obj.add_taxonomy()
    return obj

def test_taxonomy_1(neo4j):
    debug("neo4j_fixture = %s", repr(neo4j))

    dg_formatted_as_tree = neo4j.get_taxonomy_as_json()

    expected_graph = networkx.tree_graph(EXPECTED_TAXONOMY_RESULT, dict(id='id', children='children'))
    reparsed_graph = networkx.tree_graph(dg_formatted_as_tree, dict(id='id', children='children'))

    # is_isomorphic will automatically ignore the id numbers.  Note that you
    # can provide node_match function to override matching behaviour.  We don't
    # need to do so here
    assert networkx.is_isomorphic(reparsed_graph, expected_graph)

    
