import sys, urllib, time

startTime = time.clock()
link  = "https://academics.tjhsst.edu/compsci/ai/words.txt"
if len(sys.argv)>1:
   neighborWord = sys.argv[1]

numwords = 0
numedges = 0
wordsList = []
adjacencyList = {"setup": ['this', 'is for', 'default']}
hFile = urllib.urlopen(link)
for line in hFile:
   myword = line.rstrip("/n")
   wordsList.append(myword)
   numwords += 1
print "Number of Words:", numwords
   
def related(one, two):
   if(len(one) != len(two)):
      return False
   count = 0   
   for (a,b) in zip(one, two):
      if(a != b):
         count += 1
      if(count > 1):
         return False
   return True

numedges = 0
neighborList = []
for word in range(len(wordsList)):
    for wordcompare in range(word+1, len(wordsList)):
      if(wordsList[word] != wordsList[wordcompare] and related(wordsList[word], wordsList[wordcompare])):
         numedges += 2
         if wordsList[word].strip() in adjacencyList:
            backup = adjacencyList[wordsList[word].strip()]
            backup.append(wordsList[wordcompare].strip())
            adjacencyList[wordsList[word].strip()] = backup
         else:
            newlist = []
            newlist.append(wordsList[wordcompare].strip())
            adjacencyList[wordsList[word].strip()] = newlist

         if wordsList[wordcompare].strip() in adjacencyList:
            backup = adjacencyList[wordsList[wordcompare].strip()]
            backup.append(wordsList[word].strip())
            adjacencyList[wordsList[wordcompare].strip()] = backup
         else:
            newlist = []
            newlist.append(wordsList[word].strip())
            adjacencyList[wordsList[wordcompare].strip()] = newlist


         #if(word.strip() == neighborWord.strip()):
          #  neighborList.append(wordcompare.strip())

adjacencyList.pop("setup")

noNeighbors = []

for word in wordsList:
   if word.strip() not in adjacencyList:
      noNeighbors.append(word.split())
         
print "Number of Edges:", numedges/2         

maxList = []
maxWord = ""
maxLength = 0

for key in adjacencyList:
   if(len(adjacencyList[key]) > maxLength):
      maxList = adjacencyList[key]
      maxWord = key
      maxLength = len(adjacencyList[key])

print "The word with the most neighbors is " + maxWord + " and it has ", \
      maxLength, " neighbors. Those neighbors are: ", maxList


neighborSizeDistribution = {}

for key in adjacencyList:
   if len(adjacencyList[key]) in neighborSizeDistribution:
      neighborSizeDistribution[len(adjacencyList[key])] += 1
   else:
      neighborSizeDistribution[len(adjacencyList[key])] = 1

print "Neighborhood-size Frequency:"
print "0: ", len(noNeighbors)
for key in neighborSizeDistribution:
   if(neighborSizeDistribution[key] != 0):
      print key, ": ", neighborSizeDistribution[key]

print "Run time:", time.clock()-startTime
#print("Neighbors:");print(adjacencyList[neighborWord])
