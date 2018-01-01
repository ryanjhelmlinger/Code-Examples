
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
swapList = {"setup": ['this', 'is for', 'default']}

f = open('words.txt', "r")
wordsList = f.readlines()
f.close()
numwords = len(wordsList)
#print "Number of Words:", numwords


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
   #return path]

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
            pathTo = DFS(start, vertex, adjacencyList)
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

def dijkstra(start, end, graph):
   startTime = time.clock()
   alreadyVisited = set([start])
   #queueSet = set([start])
   pathWeight = {start: 0}
   path = {start: [start]}
   vertVisited = 0
   while(True):
      vertVisited += 1
      minWeightV = ""
      minWeight = len(adjacencyList)*5
      pointerV = ""
      for vertex in alreadyVisited:
         for weight in adjacencyList[vertex]:
            if weight not in alreadyVisited:
               newWeight = pathWeight[vertex] + 1
               if(minWeight > newWeight):
                  minWeight = newWeight
                  minWeightV = weight
                  pointerV = vertex
         for weight in swapList[vertex]:
            if weight not in alreadyVisited:
               newWeight = pathWeight[vertex] + 5
               if(minWeight > newWeight):
                  minWeight = newWeight
                  minWeightV = weight
                  pointerV = vertex
      #print pointerV, ", ", minWeightV, ", ", minWeight, ", ", path[vertex], ", ", pathWeight[vertex]
      if(minWeightV != ""):
         alreadyVisited.add(minWeightV)
         pathWeight[minWeightV] = minWeight
         plist = []
         for p in path[pointerV]:
            plist.append(p)
         plist.append(minWeightV)
         path[minWeightV] = plist
         if(minWeightV == end):
            break;
   print ""
   print "The minumum path between ", start, " and ", end,  " is ", pathWeight[end], " and it is: ", path[end]
   print ""
   print "The largest size of the queue was ", len(alreadyVisited)
   print ""
   print "Dijkstra visited ", vertVisited, " vertices"
   print ""
   print "Run time for Dijkstra: ", time.clock()-startTime

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


for word in wordsList:
   neighborList = []
   for i in range(0, len(word)-1):
      s = word[:i] + word[i+1:i+2] + word[i:i+1] + word[i+2:]
      if(s!=word):
         neighborList.append(s.strip())
   for value in neighborList:
      if word.strip() in swapList:
         backup = swapList[word.strip()]
         backup.append(value.strip())
         swapList[word.strip()] = backup
      else:
         newlist = []
         newlist.append(value.strip())
         swapList[word.strip()] = newlist


for key in adjacencyList:
   oldlist = adjacencyList[key]
   newlist = []
   for word in oldlist:
      if word in adjacencyList:
         newlist.append(word)
         numedges += 1
   adjacencyList[key] = newlist


for key in swapList:
   oldlist = swapList[key]
   newlist = []
   for word in oldlist:
      if word in swapList:
         newlist.append(word)
         numedges += 1
   swapList[key] = newlist


adjacencyList.pop("setup")
swapList.pop("setup")

#if(args == 1):
#   farWord = furthestWord(startWord, adjacencyList)
#   pathTo = BFS(startWord, farWord, adjacencyList)
#   print "The furthest word from ", startWord, " is ", farWord, \
#      " and the the path to it is of length ", len(pathTo), " and it is ", pathTo
#if(args == 1):
#   farWord = furthestWord(startWord.strip(), adjacencyList)
#   pathTo = DFS(startWord.strip(), farWord, adjacencyList)
#   print "The furthest word from ", startWord, " is ", farWord, \
#      " and the the path to it is of length ", len(pathTo)-1, " and it is ", pathTo


if(args == 2):
   #startTime = time.clock()
   pathTo = DFS(startWord, endWord, adjacencyList)
   if not pathTo:
      print startWord, " and ", endWord, " are not connected"
   else:
      #print "The path between ", startWord, " and ", endWord, " is of length ", \
      #len(pathTo)-1, " and it is ", pathTo

      #print ""
      #print "Run time for DFS :", time.clock()-startTime

      #print ""
      #print ""

      dijkstra(startWord, endWord, adjacencyList)
      #print ""
      #print "Run time for Dijkstra: ", time.clock()-startTime

print ""

#print "Run time:", time.clock()-startTime