import sys, urllib, time

startTime = time.clock()
#link  = "https://academics.tjhsst.edu/compsci/ai/words.txt"
#if len(sys.argv)>1:
#   neighborWord = sys.argv[1]


numwords = 0
numedges = 0
wordsList = []
adjacencyList = {"setup": ['this', 'is for', 'default']}
#hFile = urllib.urlopen(link)
#for line in hFile:
   #myword = line.rstrip("/n")
   #wordsList.append(myword)
   #numwords += 1
f = open('words.txt', "r")
wordsList = f.readlines()
f.close()
numwords = len(wordsList)
print "Number of Words:", numwords

'''   
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
'''


numedges = 0
for word in wordsList:
   neighborList = []
   for letter in "abcdefghijklmnopqrstuvwxyz":
      for i in range(0, len(word)-1):
         if(letter.strip() != word[i]):
            s = word[:i] + letter + word[i+1:]
            neighborList.append(s.strip())
   for value in neighborList:
      if word.strip() in adjacencyList:
         backup = adjacencyList[word.strip()]
         backup.append(value.strip())
         adjacencyList[word.strip()] = backup
      else:
         newlist = []
         newlist.append(value.strip())
         adjacencyList[word.strip()] = newlist


for key in adjacencyList:
   oldlist = adjacencyList[key]
   newlist = []
   for word in oldlist:
      if word in adjacencyList:
         newlist.append(word)
         numedges += 1
   adjacencyList[key] = newlist


      #adjacencyList[word.strip()] = neighborList
   #for key in adjacencyList:
    #  print key, ": ", adjacencyList[key]  

#for key in adjacencyList:
#   print key, ": ", adjacencyList[key]
#for word in wordsList:
#   word = word.strip()
#for word in wordsList:
#   print word




adjacencyList.pop("setup")


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
for key in neighborSizeDistribution:
   if(neighborSizeDistribution[key] != 0):
      print key, ": ", neighborSizeDistribution[key]

print "Run time:", time.clock()-startTime
#print("Neighbors:");print(adjacencyList[neighborWord])