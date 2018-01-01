import sys, urllib, time, queue, math, copy
from math import pi , acos , sin , cos
from random import shuffle
import numpy as np
import cv2
import urllib.request
import itertools

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


def hillClimber(series, size, distLoc, midStep):
	print("here")
	totD = cost(series, size, distLoc)
	swaps = swap(series, size)
	minCost = sys.float_info.max
	minSeries = 0
	for order in swaps:
		dist = cost(order, size, distLoc)
		if dist<minCost:
			minCost = dist
			minSeries = order
			print("------", minCost)
			print("\n")
			img = display(minSeries, midStep)
			cv2.imshow("Path", img)
			cv2.waitKey(27)
			#img = display(minSeries, midStep)
			#cv2.imshow("Path", img)
			#cv2.waitKey(27)
	if minCost<totD:
		return hillClimber(minSeries, size, distLoc, midStep)
	'''print (totD, " ", minimum)
	if totD < minimum:
		minimum = totD
		print(series)
		print(minimum)
		print("\n")
	randomize(series)
	return hillClimber(series, size, distLoc, totD)'''
	path, dist = edgeClimb(series, size, distLoc, distance, midStep)
	return (path, dist)
	#return (series, totD)

def costB(city1, city2, distLoc):
	cost = 0
	currList = distLoc[city1]
	for (place,dist) in currList:
		if place == city2:
			cost = dist
			break
	return cost

def edgeClimb(series, size, distLoc, distance, midStep, start):
	#print("here")
	totD = distance
	#finalPath = series[:]
	finalDist = distance
	#print(series)
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
				print(finalDist)
				print("\n")
				img = display(finalPath, midStep)
				cv2.imshow("Path", img)
				cv2.waitKey(27)
				return edgeClimb(finalPath, size, distLoc, finalDist, midStep, first)

	if edited == True:
		return edgeClimb(finalPath, size, distLoc, finalDist, midStep)
	else:	
		#print("sdhfajshfdsal")
		return (series, finalDist)
	#return (series, totD)

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
				if minDist<minimum:
					print(minDist)
					print("\n")
					img = display(minPath, midStep)
					cv2.imshow("Path", img)
					cv2.waitKey(27)
		series = minPath
	return (series, cost(series, size, distLoc))



def randomize(series):

	shuffle(series)

	'''copy = series[600:]
	shuffle(copy)
	series[600:] = copy
	return series'''

def display(series, midStep):
	#print(distLoc)
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
	
	#image = cv2.imread("grass.jpg", 1)

	prevLat = prevLon = -1
	for term in series:
		(lat, lon) = midStep[term]
		x = int(700*(lat-minLat)/(maxLat-minLat))+50
		y = int(700*(lon-minLon)/(maxLon-minLon))+50
		cv2.circle(image,(y,x), 2, (0,0,0), -1)
		#cv2.circle(image,(y,x-15), 5, (0,0,255), -1)
		#pts = np.array([[y-12,x-10],[y+12,x-10],[y,x-20]], np.int32) 
		#pts = pts.reshape((-1,1,2)) 
		#cv2.polylines(image,[pts],True,(0,0,255), 3)

		#cv2.rectangle(image, (y-10, x-10), (y+10, x+10), (255, 0, 0), -1)
		#cv2.circle(image,(y,x), 3, (0,0,0), -1)
		if not prevLat == -1:
			#cv2.line(image, (y, x), (prevLon, prevLat), (70, 70, 70), 10)
			#cv2.line(image, (y, x), (prevLon, prevLat), (0, 215, 255), 1)
			cv2.line(image, (y, x), (prevLon, prevLat), (0, 0, 0), 1)
		else:
			firstX, firstY = x, y
		prevLat, prevLon = x, y
	#cv2.line(image, (firstY, firstX), (prevLon, prevLat), (70, 70, 70), 10)
	#cv2.line(image, (firstY, firstX), (prevLon, prevLat), (0, 215, 255), 1)
	cv2.line(image, (firstY, firstX), (prevLon, prevLat), (0, 0, 0), 1)
	M = cv2.getRotationMatrix2D((800/2,800/2),90,1)
	dst = cv2.warpAffine(image,M,(800,800))
	return dst
	return image
	#while(True):
	#	cv2.imshow("Path", image)
	#	cv2.waitKey(27)



sys.setrecursionlimit(10000)
#(size, midStep) = readLoc("loc6.txt")
#(size, midStep) = readLoc("loc38.txt")
(size, midStep) = readLoc("loc734.txt")

distLoc = findDist(midStep)

order = []
for i in range(int(size)):
	order.append(i)

#randomize(order)

#print(costB(0, 1, distLoc))
#print(costB(1, 2, distLoc))
#print(costB(2, 0, distLoc))
#print(cost([0,1,2], 3, distLoc))


minimum = sys.float_info.max

#testList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
#display(testList, midStep)
#display
path = order
#path = [723, 692, 733, 722, 711, 691, 595, 602, 568, 567, 553, 546, 527, 501, 486, 473, 440, 408, 416, 429, 432, 436, 430, 405, 404, 372, 354, 350, 341, 333, 323, 320, 315, 297, 290, 309, 322, 340, 343, 358, 362, 382, 379, 376, 375, 346, 303, 275, 259, 272, 254, 258, 287, 286, 285, 289, 298, 310, 332, 307, 319, 306, 353, 349, 355, 388, 419, 428, 427, 444, 424, 443, 426, 465, 455, 470, 468, 495, 531, 523, 565, 633, 651, 666, 594, 593, 607, 592, 548, 544, 545, 564, 552, 539, 530, 515, 481, 494, 466, 467, 460, 463, 451, 439, 414, 402, 387, 392, 384, 395, 396, 406, 397, 398, 403, 393, 390, 381, 366, 365, 361, 348, 360, 357, 326, 318, 308, 317, 301, 296, 292, 284, 277, 278, 302, 314, 281, 274, 282, 257, 253, 249, 248, 220, 209, 203, 213, 227, 221, 215, 196, 187, 171, 157, 163, 184, 192, 205, 197, 200, 210, 216, 217, 237, 231, 224, 222, 218, 193, 182, 201, 176, 172, 140, 144, 147, 151, 143, 135, 115, 127, 128, 137, 121, 105, 100, 101, 93, 86, 98, 102, 95, 77, 63, 81, 96, 116, 113, 110, 149, 118, 111, 106, 87, 60, 58, 47, 34, 31, 29, 32, 36, 51, 56, 88, 89, 107, 112, 103, 70, 64, 69, 61, 48, 41, 37, 30, 54, 59, 68, 50, 42, 38, 39, 33, 28, 19, 13, 8, 12, 11, 14, 22, 23, 25, 27, 20, 18, 16, 9, 7, 3, 4, 6, 1, 10, 5, 2, 0, 15, 26, 17, 21, 24, 35, 44, 45, 46, 76, 92, 83, 84, 78, 79, 80, 85, 90, 114, 126, 132, 117, 109, 108, 161, 164, 168, 179, 189, 190, 194, 186, 169, 170, 183, 191, 180, 181, 208, 212, 214, 195, 211, 236, 252, 268, 261, 269, 262, 288, 280, 245, 255, 246, 256, 228, 239, 241, 247, 270, 313, 325, 324, 321, 336, 347, 352, 337, 312, 316, 295, 294, 291, 244, 207, 260, 264, 265, 293, 311, 305, 331, 342, 330, 351, 364, 389, 391, 410, 423, 394, 380, 400, 371, 386, 383, 373, 374, 356, 378, 420, 462, 448, 401, 411, 442, 425, 418, 453, 461, 464, 469, 479, 478, 484, 492, 507, 493, 489, 499, 522, 535, 525, 516, 511, 503, 475, 459, 454, 471, 482, 472, 480, 500, 514, 519, 521, 518, 512, 508, 517, 526, 543, 538, 542, 550, 558, 557, 590, 613, 622, 632, 631, 621, 617, 612, 584, 575, 571, 601, 629, 620, 611, 616, 610, 578, 574, 583, 588, 579, 589, 566, 536, 534, 498, 497, 452, 458, 446, 445, 450, 447, 438, 437, 435, 441, 421, 415, 409, 417, 407, 367, 363, 339, 335, 329, 300, 304, 279, 271, 267, 251, 235, 233, 204, 219, 226, 230, 266, 276, 283, 273, 243, 242, 238, 223, 199, 175, 177, 166, 178, 167, 162, 160, 159, 156, 141, 139, 150, 146, 142, 125, 119, 120, 123, 122, 99, 104, 71, 72, 73, 74, 75, 67, 57, 66, 62, 53, 52, 49, 43, 40, 55, 65, 94, 82, 91, 97, 124, 131, 133, 130, 136, 155, 158, 185, 198, 206, 188, 174, 165, 154, 138, 129, 134, 148, 153, 152, 145, 173, 202, 225, 240, 263, 229, 232, 234, 250, 299, 328, 327, 338, 344, 345, 334, 370, 399, 377, 369, 368, 359, 385, 413, 412, 422, 431, 433, 449, 434, 457, 474, 477, 496, 485, 506, 529, 537, 532, 533, 540, 510, 502, 487, 491, 488, 513, 541, 555, 559, 556, 600, 599, 577, 570, 561, 547, 563, 587, 585, 576, 580, 606, 636, 641, 649, 664, 670, 663, 658, 662, 654, 657, 643, 644, 645, 642, 639, 630, 614, 618, 623, 615, 609, 603, 605, 598, 591, 572, 551, 554, 528, 509, 505, 490, 483, 456, 476, 504, 520, 524, 549, 560, 562, 573, 619, 637, 624, 626, 569, 604, 608, 628, 627, 650, 653, 665, 671, 677, 687, 684, 686, 690, 696, 695, 694, 704, 703, 700, 701, 702, 706, 713, 712, 709, 707, 708, 714, 720, 719, 718, 717, 730, 729, 727, 728, 732, 731, 726, 716, 725, 724, 721, 715, 710, 705, 699, 697, 698, 689, 685, 680, 681, 673, 659, 668, 676, 656, 646, 625, 597, 586, 582, 638, 634, 635, 647, 648, 661, 672, 688, 679, 683, 669, 655, 652, 596, 581, 640, 660, 667, 678, 682, 674, 675, 693]
distance = cost(path, int(size), distLoc);
minPath = 0
first = True
while (True):
	#(path, distance) = hillClimber(order, int(size), distLoc)
	#path =  [0, 1, 3, 2, 4, 5, 6, 7, 8, 11, 10, 18, 17, 16, 15, 12, 14, 19, 22, 25, 24, 21, 23, 27, 26, 30, 35, 33, 32, 37, 36, 34, 31, 29, 28, 20, 13, 9]
	#distance = cost(path, int(size), distLoc)
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
			#for part in path:
			#	x,y = midstep[part]
			#plt.plot(x, y, marker="o", markerfacecolor="r")
			#plt.show()
		#dist = cost(path, int(size), distLoc)
		#(path, distance) = hillClimber(order, int(size), distLoc, midStep)
		(path, distance) = edgeClimb(order, int(size), distLoc, distance, midStep, 0)
		(path, distance) = edgeClimb(path, int(size), distLoc, distance, midStep, 0)
		(path, distance) = perMove(path, int(size), distLoc, midStep, distance)
		(path, distance) = edgeClimb(path, int(size), distLoc, distance, midStep, 0)
		(path, distance) = perMove(path, int(size), distLoc, midStep, distance)
		#randomize(order)
		#display(order, midStep)
		#where while ends in case want to go back

		print (path)
		print (cost(path, int(size), distLoc))

#for key in distLoc:
#	print (key, ": ", distLoc[key])
#	print ("\n")
#print(distLoc)