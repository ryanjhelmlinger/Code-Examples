import sys, urllib, time, Queue
from math import pi , acos , sin , cos

args = 0
if len(sys.argv) == 3:
	args = 2
	startWord = sys.argv[1]
	endWord = sys.argv[2]

def calcd(y1,x1, y2,x2):
   y1  = float(y1)
   x1  = float(x1)
   y2  = float(y2)
   x2  = float(x2)
   R   = 3958.76
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

def readCityLoc(filename):
	loc = {}
	count = 0
	f = open(filename, "r")
	for line in f:
		currkey = ""
		currloc = []
		for word in line.split():
			if(count == 0):
				currkey = word
				count = 1
			elif(count == 1):
				currloc.append(word)
				count = 2
			else:
				currloc.append(word)
				count = 0
				loc[currkey] = currloc
	f.close
	return loc

def readCityAdj(filename):
	adj = {}
	count= 0
	f = open(filename, "r")
	for line in f:
		onecity = ""
		twocity = ""
		currloc = []
		for word in line.split():
			if(count == 0):
				onecity = word
				count = 1
			else:
				twocity = word
				count = 0
		if onecity in adj:
			currloc = adj[onecity]
			currloc.append(twocity)
			adj[onecity] = currloc
		else:
			currloc.append(twocity)
			adj[onecity] = currloc
		currloc = []
		if twocity in adj:
			currloc = adj[twocity]
			currloc.append(onecity)
			adj[twocity] = currloc
		else:
			currloc.append(onecity)
			adj[twocity] = currloc
	f.close
	return adj

def readCityNames(filename):
	name = {}
	f = open(filename, "r")
	for line in f:
		letter = line[0]
		name[letter] = line.strip("\n")
	f.close
	return name

def mapout(loc, adj):
	rom = {}
	for key in adj:
		for word in adj[key]:
			loc1 = loc[key]
			loc2 = loc[word]
			distance = calcd(loc1[0], loc1[1], loc2[0], loc2[1])
			pathd = {word: distance}
			currloc = []
			if key in rom:
				for part in rom[key]:
					currloc.append(part)
				currloc.append(pathd)
				rom[key] = currloc
			else:
				currloc.append(pathd)
				rom[key] = currloc
	return rom
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


location = readCityLoc("romNodes.txt")
adjacency = readCityAdj("romEdges.txt")
names = readCityNames("romFullNames.txt")
rommap = mapout(location, adjacency)

print("\n")




print("\n")
