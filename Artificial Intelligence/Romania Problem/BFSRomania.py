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

def BFS(start, end, adjacencyList):
   if(start == end):
      return [start]
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
            if len(pathTo) > 1:
            	for part in pathTo:
                	path.append(part)
        	else:
        		print "\n here"
        		path.append(pathTo)
            path.append(end)
            return path
         if word not in alreadyVisited:
            queue.put(word)
            alreadyVisited.add(word)

def bfsPath(adj):
	if(args == 2):
		pathTo = BFS(startWord, endWord, adj)
    	if(len(pathTo) == 0):
    		print startWord, " and ", endWord, " are not connected"
    	else:
    		print "The path between ", startWord, " and ", endWord, " is of length ", len(pathTo)-1, \
        		" and it is ", pathTo


location = readCityLoc("romNodes.txt")
adjacency = readCityAdj("romEdges.txt")
names = readCityNames("romFullNames.txt")
rommap = mapout(location, adjacency)

print("\n")
bfsPath(adjacency)
print("\n")
