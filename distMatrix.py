import json
import numpy as np
import nltk

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def calcDist(source, target):
    scrWords = set(source['words'])
    tarWords = set(target['words'])

    unionWords = len(scrWords.union(tarWords))
    if (len(scrWords.union(tarWords)) == 0):
        unionWords = -1

    entry = {}
    entry['words'] = list(scrWords.intersection(tarWords))
    entry['score'] = len(entry['words']) / unionWords
    
    return entry
    


with open('./docs.json', 'r') as file:
    data = json.load(file)
    data = np.array(data)

distMatrix = []
allDist = []

# preprocess the words
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

# print(data[0]['words'])
for row in data:
    filtered = []
    for word in row['words']:
        word = word.lower()
        if word not in stop_words:
            filtered.append(ps.stem(word))
    row['words'] = list(set(filtered))
# print(data[0]['words'])

# store distances
for row in data:
    allDist = []
    sortedDist = []
    top10And1000 = []
    for col in data:
        entry = {}
        entry['ref'] = col['ref']
        if (row['ref'] != col['ref']):
            temp = calcDist(row, col)
            entry['dist'] = temp['score']
            entry['words'] = temp['words']
        else:
            entry['dist'] = -1
            entry['words'] = ''
        allDist.append(entry)
    sortedDist = sorted(allDist, key = lambda i: i['dist'], reverse = True)
    top10And1000.append(sortedDist[999])
    top10And1000.extend(sortedDist[:10])
    distMatrix.append(top10And1000)
    # distMatrix.append(sorted(allDist, key = lambda i: i['dist'])[-10:])

with open('./dist.json', 'w') as out:
    json.dump(distMatrix, out)
    print("Successful!")