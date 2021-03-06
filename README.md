# OCCUBROW

## Other repositories

Other repositories that are related:

* <https://github.com/amoe/amoe-butterworth-widgets>
* <https://github.com/amoe/occubrow-graph-view>
* <https://github.com/amoe/occubrow-ui>

## Setup & deployment instructions

To run the backend server, `make run_backend`.

For more detailed instructions, see [Setup Guide 2019-07](doc/SETUP_GUIDE_201907.md).

## Notes regarding 'key' property

A property 'key' was added on the Taxon node.  This is to distinguish taxons.
This property has the advantage that it makes it possible to enumerate the entire
tree faster, without traversing relationships.  However the downside is that
it means that URIs might no longer identify a Taxon uniquely.  This can cause
all kinds of problems.  The best option is to set up constraints first.

Scenario setup scripts should follow the following template:

1. Reset the schema
2. Create constraints
3. Load taxonomies
4. Create annotated corpus
5. Import annotated corpus
6. Create indexes

License: AGPL.  2019.
