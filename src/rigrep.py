import pickle
import sys

f = open(".index")
reverseIndex, filesById = pickle.load(f)

f.close()

def search(token):
	if token not in reverseIndex:
		return 
	fileNames = []
	for docId in reverseIndex[token]:
		fileNames.append(filesById[docId])
	return fileNames

print search(sys.argv[1])


