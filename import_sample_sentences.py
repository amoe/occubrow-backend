import occubrow.system
import sys
import pprint
import pdb
import bs4

backend = occubrow.system.get_backend()

def import_annotation_file(sentence_file_path):
    with open(sentence_file_path, 'r') as f:
        root = bs4.BeautifulSoup(f, 'lxml')

    sentences = root.find_all('sentence')

    for sentence in sentences:
        sentence_text = sentence.text
        sentence_id = backend.add_sentence(sentence_text)

        for annotation in sentence.find_all('annotation'):
            token = annotation.text
            reference = annotation['ref']
            backend.annotate(sentence_id, token, reference)
