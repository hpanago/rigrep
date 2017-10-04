#!/usr/bin/env python2
"""This script is used to reverse index a multitude of text files so that they
can be efficiently searched through later.

By "reverse index", we mean to
index files by the tokens they contain, instead of indexing tokens by the
files which contain them.

Usage: python2 rigrepdb.py path/to/root_directory

Here, by root_directory, we mean the root folder containing the text files we
want to index, and potentially other nested folders containing more text files
to be indexed."""

import os
import pickle
import re
import sys

from collections import defaultdict

# REVERSE_INDEX contains token : {set of doc_id's} key-value pairs.
# Here, every file to be indexed is assigned a doc_id, and the path of the
# file corresponding to a given doc_id can be found in FILES_BY_ID.
# FILES_BY_ID contains doc_id : file path  key-value pairs.
REVERSE_INDEX = defaultdict(set)  # Uninitialized value defaults to empty set.
FILES_BY_ID = {}


def index_doc(name):
    """Indexes a file (whose file name is passed) by reading the tokens
    (keywords) it contains and reverse indexing them."""

    with open(name, 'r') as search_file:
        document = search_file.read()
        doc_id = list_file(name)
        for token in tokenizer(document):
            REVERSE_INDEX[token].add(doc_id)
    return REVERSE_INDEX


# Used for tokenizing (splitting) text file contents.
SPLITTER = re.compile(r"[\s\W]+")


def tokenizer(document):
    """Uses the tokenizer SPLITTER defined globally to split the contents of
    the passed document into words."""

    tokens = SPLITTER.split(document)
    return tokens


def list_file(name):
    """Assigns an ID to the file (whose filename is passed) so that it can be
    indexed in FILES_BY_ID for lookups. Thus, this function also modifies
    FILES_BY_ID"""

    full_path = os.path.abspath(name)
    doc_id = len(FILES_BY_ID)
    FILES_BY_ID[doc_id] = full_path
    return doc_id


# Traverses through the root directory passed by the user via command line to
# index the contained text files.
for root, dirs, files in os.walk(sys.argv[1], topdown=False):
    for file_name in files:
        if file_name[0] == '.':
            continue
        index_doc(os.path.join(root, file_name))


# Dumps the indexing into the .index file.
with open('.index', 'wb+') as index_file:
    pickle.dump((REVERSE_INDEX, FILES_BY_ID), index_file)
