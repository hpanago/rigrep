#!/usr/bin/env python2
"""This script specifies a command line tool to get the files containing a
specified keyword.
Usage: python2 rigrep.py <keyword>
Here, <keyword> is the word you want to search."""

import pickle
import sys


def search(token):
	"""Searches for files containing the passed token using the .index file
	and returns the list of their names."""

	if token not in reverse_index:
		return None  # Return if token is not in reverse_index, as it means
	                 # the token is absent in all the files.
	file_names = []
	for doc_id in reverse_index[token]:
		file_names.append(files_by_id[doc_id])
	return file_names


# Loads the pickled index file into memory.
# Thus, it's not memory-friendly and better ways must be devised.
with open(".index", "rb") as f:
	reverse_index, files_by_id = pickle.load(f)

# Output can be dramatically better if it is in a tree structure.
# But for now, just a linear loop is used.
results = search(sys.argv[1])
if results is not None:
	for result in search(sys.argv[1]):  # Displays the results nicely.
		print(result)
