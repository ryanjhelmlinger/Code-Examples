import sys, urllib, time, Queue
from math import pi , acos , sin , cos


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

def astar(start, end, graph, location):
	startTime = time.clock()
	aopen = set([start])
	aclose = set([])
	loc1 = location[start]
	loc2 = location[end]
	dist = calcd(loc1[0], loc1[1], loc2[0], loc2[1])
	costDict = {start: [dist, dist]}
	parent = {}
	maxQ = 0
	while(True):
		lowF = sys.maxint
		lowH = sys.maxint
		lowNode = ""
		for node in aopen:
			cost = costDict[node]
			if (cost[0] < lowF) or (cost[0] == lowF and cost[1] < lowH):
				lowNode = node
				lowF = cost[0]
				lowH = cost[1]
		aopen.remove(lowNode)
		aclose.add(lowNode)

		if len(aopen) > maxQ:
			maxQ = len(aopen)

		if lowNode == end:
			break

		for neighbor in graph[lowNode]:
			for key in neighbor:
					city = key
					dist = neighbor[key]
			if city not in aclose:
				cost = costDict[lowNode]
				g = (cost[0]-cost[1]) + dist
				loc1 = location[city]
				loc2 = location[end]
				h = calcd(loc1[0], loc1[1], loc2[0], loc2[1])
				f = g + h
				if city in aopen:
					prevCost = costDict[city]
					if (f < prevCost[0]) or (prevCost[0] == f and h < prevCost[1]):
						costDict[city] = [f, h]
						parent[city] = lowNode
				else:
					costDict[city] = [f, h]
					parent[city] = lowNode
				if city not in aopen:
					aopen.add(city)

	pathHelp = []
	pathPart = end
	while pathPart in parent:
		pathHelp.append(pathPart)
		pathPart = parent[pathPart]
	path = [start]
	while len(pathHelp) > 0:
		path.append(pathHelp.pop())

	cost = costDict[end]

	print ""
	print "The minumum path between ", start, " and ", end,  " is ", cost[0], " and it is: ", path
	print ""
	print "The largest size of the queue was ", maxQ
	print ""
	print "Dijkstra visited ", len(aclose), " vertices"
	print ""
	print "Run time for Dijkstra: ", time.clock()-startTime
	return 0;





location = readCityLoc("romNodes.txt")
adjacency = readCityAdj("romEdges.txt")
names = readCityNames("romFullNames.txt")
rommap = mapout(location, adjacency)

print("\n")
if len(sys.argv) == 3:
	astar(sys.argv[1], sys.argv[2], rommap, location)
print("\n")