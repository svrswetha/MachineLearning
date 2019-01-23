from collections import Counter
import os, math, random, re

pathDir = os.listdir(os.getcwd() + '/newsgroups')
fileList = {}
testingSet = {}
trainingSet = {}
for folderName in pathDir:
    appendingPath = os.getcwd() + '/newsgroups/' + folderName + '/'
    pathFile = os.listdir(os.getcwd() + '/newsgroups/' + folderName)
    fileList[folderName] = pathFile
    randomList = range(0, len(pathFile))
    random.shuffle(randomList)
    # 50-50 split for training & testing
    trainingSet[folderName] = list(map(lambda x: pathFile[x], randomList[(len(pathFile) / 2):]))
    testingSet[folderName] = list(map(lambda x: appendingPath + pathFile[x], randomList[:(len(pathFile) / 2)]))

# Regular Expression for words
def readingWords(file):
    with open(file, 'r') as word:
        strings = word.read().lower()
        return re.findall(r"[\w']+", strings)

# probability of the class words by avoiding zero probability error
def wordProbabiity(hash, word, den):
    word = word.lower()
    if word in hash:
        return math.log(hash[word] + 1.0) / den
    return math.log(1.0 / den)

# Total Probability calculation
def totalProbability(file, hash, den):
    li = list(map(lambda x: wordProbabiity(hash, x, den), readingWords(file)))
    return reduce(lambda x, y: x + y, li)

# classification
def classification(file, hashing, traningSum, counter):
    print(file)
    keys = traningSum.keys()
    probability = list(map(lambda x: totalProbability(file, hashing[x], trainingSum[x] + counter), keys))
    minimumValue = min(probability)
    maximumValue = max(probability)
    probability = list(map(lambda x: x - maximumValue, probability))
    den = sum(list(map(lambda x: math.exp(x), probability)))
    probability = list(map(lambda x: math.exp(x) / den, probability))
    maximumValue = max(probability)
    print(maximumValue)
    maximumIndex = [index for index in range(len(probability)) if probability[index] == maximumValue]
    if (len(maximumIndex) > 1):
        print 'Cannot classify as it has the same probability'
    return keys[maximumIndex[0]]

# Unique Word Counting
uniqueWordCount = dict(zip(pathDir, list(map(lambda x: len(fileList[x]), pathDir))))
trainingCount = {}
count = Counter()
trainingSum = {}
for key in pathDir:
    print key
    cwd = os.getcwd() + '/newsgroups/' + key + '/'
    cnt = Counter()
    for fi in trainingSet[key]:
        cnt = cnt + Counter(readingWords(cwd + str(fi)))
    count = count + cnt
    trainingCount[key] = dict(cnt)
    trainingSum[key] = sum(trainingCount[key].values())
count = len(dict(count).keys())

# Classifying test data using the trained model
print(testingSet.keys()[0])
length = len(testingSet.keys())
for i in range(0, length):
    fileLength = len(testingSet[testingSet.keys()[i]])
    for j in range(0, fileLength):
        print(" Classifying the testing feature")
        print(classification(testingSet[testingSet.keys()[i]][j], trainingCount, trainingSum, count))
