import json, string

with open('./fullData.json', 'r') as file:
    data = json.load(file)

abstracts = []
for row in data:
    abstracts.append(row['AB'])

# print(abstracts[0].translate(str.maketrans('','',string.punctuation)))
docs = []
for abstract in abstracts:
    wordList = abstract.translate(str.maketrans('','',string.punctuation)).split()
    docs.append(set(wordList))

docData = []
for i, doc in enumerate(docs):
    entry = {}
    entry['ref'] = i
    entry['words'] = list(doc)
    docData.append(entry)

with open('docs.json', 'w') as outFile:
    json.dump(docData, outFile)

# print(docData)
# print(abstracts[0])