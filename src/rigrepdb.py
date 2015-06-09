import os
import sys
import pickle
import re

reverseIndex = {}
filesById = {}

def indexDoc(name):
	f = open(name,'r')
	document = f.read()
	docId = listFile(name)
	for token in tokenizer(document):
		if token in reverseIndex: 
			reverseIndex[token].add(docId)
		else:
			reverseIndex[token] = set([docId])
	f.close()
	return reverseIndex

splitter = re.compile("[\s\W]+")

def tokenizer(document):
	tokens = splitter.split(document)
	return tokens 

def listFile(name):
	fullPath = os.path.abspath(name)
	docId = len(filesById)
	filesById[docId] = fullPath
	return docId

for root, dirs, files in os.walk(sys.argv[1], topdown=False):
	for name in files:
		if name[0] == '.':
			continue
		indexDoc(os.path.join(root, name))

f = open('.index','wr')		
pickle.dump((reverseIndex, filesById),f)
f.close()