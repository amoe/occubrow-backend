import taxonomy_inserter
from occubrow.formats.thematic_categories_xlsx import SamuelsLoader
import neo4j
import sys
from occubrow.drawing import quickplot

driver = neo4j.GraphDatabase.driver("bolt://localhost:7688", auth=('neo4j', 'password'))
ti = taxonomy_inserter.TaxonomyInserter(driver)

loader = SamuelsLoader()
g = loader.load(sys.argv[1])



for n, data in g.nodes(data=True):
    if not data:
        print("id is '%s'" % n)


#ti.load_taxonomy(g)
