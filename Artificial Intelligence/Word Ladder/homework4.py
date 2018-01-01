
import sys, urllib, time, Queue

startTime = time.clock()
args = 0
if len(sys.argv) == 2:
   startWord = sys.argv[1]
   args = 1
if len(sys.argv) == 3:
   args = 2
   startWord = sys.argv[1]
   endWord = sys.argv[2]


numwords = 0
numedges = 0
wordsList = []
adjacencyList = {"setup": ['this', 'is for', 'default']}

f = open('words.txt', "r")
wordsList = f.readlines()
f.close()
numwords = len(wordsList)
print "Number of Words:", numwords


def BFS(start, end, adjacencyList):
   if(start == end):
      return start
   queue = Queue.Queue()
   path = []
   queue.put(start)
   alreadyVisited = set([start])
   while not queue.empty():
      vertex = queue.get()
      keylist = adjacencyList[vertex]
      for word in keylist:
         if(word == end):
            keylisy = []
            pathTo = BFS(start, vertex, adjacencyList)
            isString = False
            for part in pathTo:
               if(len(part) == 1):
                  isString = True
            if(isString == True):
               path.append(pathTo)
            else:
               for part in pathTo:
                  path.append(part)
            path.append(end)
            return path
         if word not in alreadyVisited:
            queue.put(word)
            alreadyVisited.add(word)
   #return path

def DFS(start, end, adjacencyList):
   if(start == end):
      return start
   stack = []
   path = []
   stack.append(start)
   alreadyVisited = set([start])
   while(len(stack) != 0):
      vertex = stack.pop()
      keylist = adjacencyList[vertex]
      for word in keylist:
         if(word == end):
            keylisy = []
            pathTo = BFS(start, vertex, adjacencyList)
            isString = False
            for part in pathTo:
               if(len(part) == 1):
                  isString = True
            if(isString == True):
               path.append(pathTo)
            else:
               for part in pathTo:
                  path.append(part)
            path.append(end)
            return path
         if word not in alreadyVisited:
            stack.append(word)
            alreadyVisited.add(word)
   #return path

def furthestWord(start, adjacencyList):
   queue = Queue.Queue()
   path = []
   queue.put(start)
   alreadyVisited = set([start])
   while not queue.empty():
      vertex = queue.get()
      keylist = adjacencyList[vertex]
      for word in keylist:
         if word not in alreadyVisited:
            queue.put(word)
            alreadyVisited.add(word)
   return vertex


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


components = {}
inComponents = set([])
q = Queue.Queue()
componentCount = 0
for key in adjacencyList:
   if key not in inComponents:
      componentCount += 1
      q.put(key)
      while not q.empty():
         vertex = q.get()
         if key in components:
            compback = components[key]
            compback.append(vertex)
            components[key] = compback
         else:
            newlist = []
            newlist.append(vertex)
            components[key] = newlist
         inComponents.add(vertex)
         for word in adjacencyList[vertex]:
            if word not in inComponents:
               q.put(word)
               inComponents.add(word)

componentsFrequency = {}
alreadyCounted = set([])
for key in components:
   if key not in alreadyCounted:
      for word in components[key]:
         alreadyCounted.add(word)
      if len(components[key]) in componentsFrequency:
         newcount = componentsFrequency[len(components[key])] + 1
         componentsFrequency[len(components[key])] = newcount
      else:
         componentsFrequency[len(components[key])] = 1


print "Number of Components: ", componentCount

for key in componentsFrequency:
   print key, ": ", componentsFrequency[key]


if(args == 1):
   farWord = furthestWord(startWord, adjacencyList)
   pathTo = BFS(startWord, farWord, adjacencyList)
   print "The furthest word from ", startWord, " is ", farWord, \
      " and the the path to it is of length ", len(pathTo)-1, " and it is ", pathTo
#if(args == 1):
#   farWord = furthestWord(startWord, adjacencyList)
#   pathTo = DFS(startWord, farWord, adjacencyList)
#   print "The furthest word from ", startWord, " is ", farWord, \
#      " and the the path to it is of length ", len(pathTo), " and it is ", pathTo
if(args == 2):
   pathTo = BFS(startWord, endWord, adjacencyList)
   if(len(pathTo) == 0):
      print startWord, " and ", endWord, " are not connected"
   else:
      print "The path between ", startWord, " and ", endWord, " is of length ", len(pathTo)-1, \
         " and it is ", pathTo


print "Run time:", time.clock()-startTime