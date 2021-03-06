import occubrow.system
import occubrow.taxonomy.taxonomy_inserter
from occubrow.formats.thematic_categories_xlsx import SamuelsLoader
from occubrow.corpus.ob_samuels_csv import OBSamuelsCSVLoader
from occubrow.corpus.import_sample_sentences import import_annotation_file
from load_stop_words import load_stop_words
import sys
import neo4j
from occubrow.neo4j_schema_utilities \
  import reset_schema, create_constraints, create_indexes

# roughly optimal for demo purposes
SAMPLING_PROBABILITY = 0.001
SAMUELS_CSV_PATH = "/home/amoe/dev/samdist/intermediate_data/m_nonl_combined.csv"

driver = neo4j.GraphDatabase.driver("bolt://localhost:7688", auth=('neo4j', 'password'))

reset_schema(driver)
create_constraints(driver)
create_indexes(driver)

ti = occubrow.taxonomy.taxonomy_inserter.TaxonomyInserter(driver)

backend = occubrow.system.get_backend()
backend.clear_all_data()


loader = SamuelsLoader()
g = loader.load("resources/media_405073_en.xlsx")
ti.load_taxonomy(g, 'theme')

loader2 = OBSamuelsCSVLoader(SAMPLING_PROBABILITY)

# The annotated file here is a temporary output, containing the sampled data.

loader2.run(SAMUELS_CSV_PATH, 'samuels-annotated.xml')

import_annotation_file('samuels-annotated.xml')

load_stop_words()
