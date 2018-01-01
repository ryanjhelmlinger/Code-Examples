import sys, urllib

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
   numwords = numwords + 1
print("Number of Words:");print(numwords)
   
def related(one, two):
   if(len(one) != len(two)):
      return False
   count = 0   
   for (a,b) in zip(one, two):
      if(a != b):
         count = count + 1
      if(count > 1):
         return False
   return True

numedges = 0
neighborList = []
for word in wordsList:
    for wordcompare in wordsList:
      if(word != wordcompare and related(word, wordcompare)):
         numedges = numedges+ 1
         if word.strip() in adjacencyList:
            backup = adjacencyList[word.strip()]
            backup.append(wordcompare.strip())
            adjacencyList[word.strip()] = backup
         else:
            newlist = []
            newlist.append(wordcompare.strip())
            adjacencyList[word.strip()] = newlist
         if(word.strip() == neighborWord.strip()):
            neighborList.append(wordcompare.strip())
         
print("Number of Edges:");print(numedges/2)         

print("Neighbors:");print(adjacencyList[neighborWord])
