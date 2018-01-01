import sys, urllib, time, queue, math, copy, random
from math import pi , acos , sin , cos
from random import shuffle
import numpy as np
import cv2
import urllib.request
import itertools
from random import randint

def readLoc(filename):
	loc = {}
	f = open(filename, "r")
	mainCount = 0
	for line in f: 
		if mainCount == 0:
			size = line
		else:
			count = 0
			for word in line.split():
				name = mainCount-1
				if count==0:
					lat = float(word)
				if count == 1:
					lon = float(word)
				count += 1
			loc[name] = (lat, lon)
		mainCount+=1
	return size, loc

def findDist(midStep):
	distLoc = {}
	for steps in midStep:
		(lat, lon) = midStep[steps] 
		for place in midStep:
			(lat1, lon1) = midStep[place] 
			if not place == steps:
				#print(steps, " ", place)
				if steps in distLoc:
					alreadyDone = distLoc[steps]
					distance = math.sqrt((lat-lat1)*(lat-lat1)+(lon-lon1)*(lon-lon1))
					alreadyDone.append((place, distance))
					distLoc[steps] = alreadyDone
				else:
					distance = math.sqrt((lat-lat1)*(lat-lat1)+(lon-lon1)*(lon-lon1))
					distLoc[steps] = [(place, distance)]
					#distLoc[place] = [(place, calcd(lon, lat, lon1, lat1))]
	return distLoc

def cost(series, size, distLoc):
	first = True
	totalSum = 0
	current = previous = start = -1
	for city in series:
		current = city
		if not previous == -1:
			currList = distLoc[city]
			for (place,dist) in currList:
				if place == previous:
					totalSum += dist
					break
		previous = current
		if first == True:
			first = False
			start = current
	currList = distLoc[start]
	for (place,dist) in currList:
		if place == previous:
			totalSum += dist
			break
	return totalSum

def costwo(series, size, distLoc):
	first = True
	totalSum = 0
	current = previous = start = -1
	for city in series:
		current = city
		if not previous == -1:
			currList = distLoc[city]
			for (place,dist) in currList:
				if place == previous:
					totalSum += dist
					break
		previous = current
		if first == True:
			first = False
			start = current
	return totalSum

def costB(city1, city2, distLoc):
	cost = 0
	currList = distLoc[city1]
	for (place,dist) in currList:
		if place == city2:
			cost = dist
			break
	return cost

def swap(series, n):
	swaps = []
	for x in range(n):
		for y in range(1, n):
			if x+y<n:
				#new = copy.copy(series)
				new = series[:]
				temp = new[x]
				new[x] = new[x+y]
				new[x+y] = temp
				swaps.append(new)
	return swaps

'''def perMove(series, size, distLoc, midStep, minimum):
	minDist = cost(series, size, distLoc)
	minPath = series
	for city in range(1,size-4):
		allPerm = list(itertools.permutations(series[city:city+4], 4))
		for perm in allPerm:
			#print(series)
			#print(perm)
			path = series[0:city]+list(perm)+series[city+4:size]
			dist = cost(path, size, distLoc)
			if dist<minDist:
				minDist = dist
				minPath = path
				if minDist<minimum:
					print(minDist)
					print("\n")
					img = display(minPath, midStep)
					cv2.imshow("Path", img)
					cv2.waitKey(27)
		series = minPath
	return (series, cost(series, size, distLoc))'''

def display(series, midStep):
	minLat = minLon = sys.float_info.max
	maxLat = maxLon = sys.float_info.min
	iLatMin = iLonMin = iLatMax = iLonMax = 0
	for key in midStep:
		lat, lon = midStep[key]
		if lat<minLat:
			minLat = lat
			iLatMin = iLatMin
		if lat>maxLat:
			maxLat = lat
			iLatMax = iLatMax
		if lon<minLon:
			minLon = lon
			iLonMin = iLonMin
		if lon>maxLon:
			maxLon = lon
			iLonMax = iLonMax
	image = np.zeros((800,800,3), np.uint8)
	image.fill(255)
	prevLat = prevLon = -1
	for term in series:
		(lat, lon) = midStep[term]
		x = int(700*(lat-minLat)/(maxLat-minLat))+50
		y = int(700*(lon-minLon)/(maxLon-minLon))+50
		cv2.circle(image,(y,x), 2, (0,0,0), -1)
		if not prevLat == -1:
			cv2.line(image, (y, x), (prevLon, prevLat), (0, 0, 0), 1)
		else:
			firstX, firstY = x, y
		prevLat, prevLon = x, y
	cv2.line(image, (firstY, firstX), (prevLon, prevLat), (0, 0, 0), 1)
	M = cv2.getRotationMatrix2D((800/2,800/2),90,1)
	dst = cv2.warpAffine(image,M,(800,800))
	return dst
	return image

def edgeClimb(series, size, distLoc, distance, midStep, start, quick):
	#print("here")
	totD = distance
	#finalPath = series[:]
	finalDist = distance
	#print(series)
	edited = True
	while(edited==True):
		edited = False
		for first in range(start, size):
			for second in range(first+2, size):
				#list2 = series[first:second+1]
				#list2 = list2[::-1]
				#new = series[:first]+list2+series[second+1:]

				if first==0 and second==size-1:
					a = 0
					b = 0
					c = 0
					d = 0
				elif not (first == 0 or second==size-1):
					a = costB(series[first-1], series[first], distLoc)
					b = costB(series[second], series[second+1], distLoc)
					c = costB(series[first-1], series[second], distLoc)
					d = costB(series[first], series[second+1], distLoc)
				elif first==0 :
					a = costB(series[len(series)-1], series[first], distLoc)
					b = costB(series[second], series[second+1], distLoc)
					c = costB(series[len(series)-1], series[second], distLoc)
					d = costB(series[first], series[second+1], distLoc)
				else:
					a = costB(series[first-1], series[first], distLoc)
					b = costB(series[second], series[0], distLoc)
					c = costB(series[first-1], series[second], distLoc)
					d = costB(series[first], series[0], distLoc)

				dist = totD-a-b+c+d
				#dist3 = cost(new, size, distLoc)

				if dist<finalDist:
					list2 = series[first:second+1]
					list2 = list2[::-1]
					new = series[:first]+list2+series[second+1:]
					edited = True
					finalPath = new[:]
					finalDist = dist
					#print(finalPath)
					#print(finalDist)
					#print("\n")
					#img = display(finalPath, midStep)
					#cv2.imshow("Path", img)
					#cv2.waitKey(27)
					#return edgeClimb(finalPath, size, distLoc, finalDist, midStep, first)
					if quick ==True: start=first
					totD = finalDist
					series = finalPath
					continue
	#else:	
		#print("sdhfajshfdsal")
	return (series, finalDist)
	#return (series, totD)

def combine(padre, madre, size, population):
	par1, ignore = padre
	par2, ignore2 = madre
	split = randint(0, size-1)
	if split>int(size*.5): 
		part2 = par1[split:]
		shuffle(part2)
		child = par1[:split] + part2
	else:
		part2 = par1[:split]
		shuffle(part2) 
		child = part2 + (par1[split:])
	if randint(0,8)==0:
		one = randint(0,size-1)
		two = randint(0,size-1)
		temp = child[one]
		child[one] = child[two]
		child[two] = temp
	dist = cost(child, size, distLoc)
	#if i<ignore and i<ignore2:
	#	print(ignore, " ", ignore2, " ", cost(child, size))
	#else:
	#	print("bad")

	child, dist = edgeClimb(child, size, distLoc, dist, midStep, 0, True)
	for person,i in population:
		if child == person:
			return combine(padre, madre, size, population)
	#print(par1, " ", ignore)
	#print(child, " ", dist)
	#print("\n")
	return (child, dist)

def perMove(series, size, distLoc, midStep, minimum):
	minDist = cost(series, size, distLoc)
	minPath = series
	for city in range(1,size-4):
		allPerm = list(itertools.permutations(series[city:city+4], 4))
		for perm in allPerm:
			#print(series)
			#print(perm)
			path = series[0:city]+list(perm)+series[city+4:size]
			dist = cost(path, size, distLoc)
			if dist<minDist:
				minDist = dist
				minPath = path
				#if minDist<minimum:
					#print(minDist)
					#print("\n")
					#img = display(minPath, midStep)
					#cv2.imshow("Path", img)
					#cv2.waitKey(27)
		series = minPath
	return (series, cost(series, size, distLoc))


def nextGeneration(population, size, pool, mini):
	parents = []
	for order,cross in population:
		if randint(0,int(cross-mini)+1)==0:
			parents.append((order,cross))
			#population.remove((order,cross))
	x=1
	while x<len(parents):
		population.append(combine(parents[x-1], parents[x], size, population))
		x+=1
	while len(population)>pool:
		minInt = 0
		badpath = 0
		for order,cross in population:
			if cross>minInt:
				badpath = order
				minInt = cross
		population.remove((badpath,minInt))
	while len(population)<pool:
		array = random.sample(range(n),n)
		population.append((array,cost(array,n)))
	return population



sys.setrecursionlimit(10000)
#(size, midStep) = readLoc("loc6.txt")
#(size, midStep), n = readLoc("loc38.txt"), 38
(size, midStep), n = readLoc("loc734.txt"), 734

popSize = 15

distLoc = findDist(midStep)
minDist = sys.float_info.max
overminPath = 0

startTime = time.clock()

population = []
for i in range(0,popSize):
	print(i)
	array = random.sample(range(n),n)
	dist = cost(array,n,distLoc)
	array, dist = edgeClimb(array, n, distLoc, dist, midStep, 0, True)
	population.append((array,dist))

afterInitialTime = time.clock()
iters = 0

while(True):
	iters+=1
	#print("Here")
	minNum=n*n*n
	minPath=0
	for person,cross in population:
		if cross<minNum: 
			minNum=cross
			minPath=person
	if minNum<minDist:
		minDist=minNum
		overminPath=minPath
		print(minDist, "\n")
		print(overminPath)
		print("Time: ", time.clock()-startTime)
		print("After initial time: ", time.clock()-afterInitialTime)
		print("\n\n")
		img = display(overminPath, midStep)
		cv2.imshow("Path", img)
		cv2.waitKey(27)
	if time.clock()-afterInitialTime > 1200:
		break
	population = nextGeneration(population, n, popSize, minNum)


print("\n\n\n\n")

array, dist = edgeClimb(overminPath, n, distLoc, minDist, midStep, 0, False)
(array, dist) = perMove(overminPath, n, distLoc, midStep, minDist)

print(array)
print("Distance: ", dist)
print("Iterations through:", iters)
print ("Run time: ", time.clock()-startTime)
while(True):
	img = display(overminPath, midStep)
	cv2.imshow("Path", img)
	cv2.waitKey(27)





#order = []
#for i in range(int(size)):
#	order.append(i)

'''minimum = sys.float_info.max

path = order
distance = cost(path, int(size), distLoc);
minPath = 0
first = True
while (True):
	if first==True:
		first = False
		if distance < minimum:
			minimum = distance
			minPath = path
			print(minPath)
			print(minimum)
			print("\n")
			img = display(path, midStep)
			cv2.imshow("Path", img)
			cv2.waitKey(27)

		#(path, distance) = edgeClimb(order, int(size), distLoc, distance, midStep, 0)
		#(path, distance) = edgeClimb(path, int(size), distLoc, distance, midStep, 0)
		#(path, distance) = perMove(path, int(size), distLoc, midStep, distance)
		#(path, distance) = edgeClimb(path, int(size), distLoc, distance, midStep, 0)
		#(path, distance) = perMove(path, int(size), distLoc, midStep, distance)

		print (path)
		print (cost(path, int(size), distLoc))'''