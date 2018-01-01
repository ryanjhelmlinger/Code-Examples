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
		count = 0
		first = 0
		cityname = ""
		for word in line.split():
			if count == 0:
				city = word
				count = 1
			else:
				if first == 0:
					cityname = cityname + word
					first = 1
				else:
					cityname = cityname + " " + word
		name[cityname] = city
	f.close
	return name

def mapout(loc, adj):
	us = {}
	for key in adj:
		for word in adj[key]:
			loc1 = loc[key]
			loc2 = loc[word]
			distance = calcd(loc1[0], loc1[1], loc2[0], loc2[1])
			pathd = {word: distance}
			currloc = []
			if key in us:
				for part in us[key]:
					currloc.append(part)
				currloc.append(pathd)
				us[key] = currloc
			else:
				currloc.append(pathd)
				us[key] = currloc
	return us



def BFS(start, end, graph):
	startTime = time.clock()
	alreadyVisited = set([start])
	pq = set([start])
	pathWeight = {start: 0}
	path = {start: [start]}
	maxQ = 0
	while(True):
		minWeightV = ""
		minWeight = sys.float_info.max
		pointerV = ""
		remove = set([])
		if len(pq) > maxQ:
			maxQ = len(pq)
		for place in pq:
			count = 0
			for cityloc in graph[place]:
				for key in cityloc:
					city = key
					dist = cityloc[key]
				if city not in alreadyVisited:
					count = 1
			if(count == 0):
				remove.add(place)
		for place in remove:
			pq.remove(place)
		for place in pq:
			for cityloc in graph[place]:
				for key in cityloc:
					city = key
					dist = 1
				if city not in alreadyVisited:
					newWeight = pathWeight[place] + dist
					if minWeight > newWeight:
						minWeight = newWeight
						minWeightV = city
						pointerV = place
		if(minWeightV != ""):
			pq.add(minWeightV)
			alreadyVisited.add(minWeightV)
			pathWeight[minWeightV] = minWeight
			plist = []
			for p in path[pointerV]:
				plist.append(p)
			plist.append(minWeightV)
			path[minWeightV] = plist
			if(minWeightV == end):
				break
	print ""
	print "The minumum path between ", start, " and ", end,  " is ", pathWeight[end], " and it is: ", path[end]
	print ""
	print "The largest size of the queue was ", maxQ
	print ""
	print "BFS visited ", len(alreadyVisited), " vertices"
	print ""
	print "Run time for BFS: ", time.clock()-startTime
	return 0;


'''def BFS(start, end, adjacencyList):
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
                path.append(part)
            path.append(end)
            return path
         if word not in alreadyVisited:
            queue.put(word)
            alreadyVisited.add(word)'''


location = readCityLoc("rrNodes.txt")
adjacency = readCityAdj("rrEdges.txt")
names = readCityNames("rrNodeCity.txt")
usmap = mapout(location, adjacency)

print("\n")

if len(sys.argv) > 3:
	if sys.argv[1] in names:
		startCity = names[sys.argv[1]]
		if sys.argv[2] in names:
			endCity = names[sys.argv[2]]
		else:
			endCity = names[sys.argv[2] + " " + sys.argv[3]]
	else:
		startCity = names[sys.argv[1] + " " + sys.argv[2]]
		if sys.argv[3] in names:
			endCity = names[sys.argv[3]]
		else:
			endCity = names[sys.argv[3] + " " + sys.argv[4]]
	BFS(startCity, endCity, usmap)
print("\n")