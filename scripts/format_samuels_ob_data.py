#! /usr/bin/env python3

# The input for this is CSV files from Julie in the format 

# These are mechanically derived from the output of the Samuels tagger, whose
# input was sharonhoward's OBV corpus.

# The text is segmented into chunks

# We want to get from here to a series of labelled tokens that know how to refer
# back to their source.  The source should be represented as a Context object
# The full source can be depicted as a URL and an xpath?

import pandas
import sys
import bs4

combined_csv_path = sys.argv[1]
df = pandas.read_csv(combined_csv_path)

result = df.groupby('chunk')

soup = bs4.BeautifulSoup(features='xml')

root = soup.new_tag("root")
soup.append(root)

for name, group in result:
    sentence = soup.new_tag('sentence')

    for index, row in group.iterrows():
        annotation_tag = soup.new_tag("annotation")
        annotation_tag['SEMTAG3'] = row['SEMTAG3']
        annotation_tag.string = row['vard']

        sentence.append(annotation_tag)
        sentence.append(" ")

    root.append(sentence)

        # Get back to the relatively pristine phrase with this.
#        print(group['vard'].str.cat(sep=' '))
        # From here we know the overall phrase (sentence)
        # and we also know the taxonomical class of each token
        # so all that remains is to produce an importable form

        # What importable form can we produce?
        # LOAD CSV format can be used.
        # It would really be worth freezing the documentation for n4j and
        # n4j pytohn driver.
        # We can easily write a testable taxonomy importer.



# So the problem with this is that once we have the data we need some way to
# link it into the existing taxonomy.

# So produce an XML-annotated set

#"18000528-0074"

sys.stdout.write(soup.prettify())