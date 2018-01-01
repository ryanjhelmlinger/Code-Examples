import sys, random, copy

numShuffles = numSwaps = percentFlat = numShuffles2 = numSwaps2 = 0

def display(series, n):
	for r in range(n):
		for c in range(n):
			if r == int(series[c]): print ("*", end=' ')
			else: print ("-", end=' ')
		print("")

def intersect(series, n):
	#print(series)
	intersects = {}
	for r in range(n):
		c1 = c2 = series[r]
		while r > 0:
			r -= 1
			c1 -= 1
			c2 += 1
		while r < n-1:
			if series[r]==c1 and not c1==c2:
				if r*n+c1 in intersects: intersects[r*n+c1] += 1
				else: intersects[r*n+c1] = 1
			if series[r]==c2 and not c1==c2:
				if r*n+c2 in intersects: intersects[r*n+c2] += 1
				else: intersects[r*n+c2] = 1
			c1 += 1
			c2 -= 1
			r += 1
	maxIntersect = 0
	for key in intersects:
		#print (intersects[key], end=' ')
		maxIntersect += intersects[key]
		#if intersects[key]>maxIntersect: maxIntersect = intersects[key]
	#print()
	#print(maxIntersect)
	return maxIntersect

def swap2(series, n, turn):
	global numSwaps
	global numSwaps2
	swapped = set([])
	for dist in range(1, n):
		for loc in range(0, n):
			if loc+dist<n:
				if turn==1: numSwaps += 1
				if turn==2: numSwaps2 += 1
				numSwaps += 1
				temp1, temp2 = series[loc], series[loc+dist]
				newOrder = series[:loc]+temp2+series[loc+1:loc+dist]+temp1+series[loc+dist+1:]
				swapped.add(newOrder)
	return swapped


def swap(series, n, turn):
	global numSwaps
	global numSwaps2
	if turn==1: numSwaps += 1
	if turn==2: numSwaps2 += 1
	swapped = []
	for dist in range(1, n):
		for loc in range(0, n):
			if loc+dist<n:
				#if turn==1: numSwaps += 1
				#if turn==2: numSwaps2 += 1
				newOrder = copy.copy(series)
				numSwaps += 1
				temp1 = newOrder[loc]
				newOrder[loc] = newOrder[loc+dist]
				newOrder[loc+dist] = temp1
				#newOrder = series[:loc]+temp2+series[loc+1:loc+dist]+temp1+series[loc+dist+1:]
				swapped.append(newOrder)
	return swapped


def randomize(series, n):
	#global numShuffles
	#numShuffles+=1
	#l = list(series)
	#print(series)
	random.shuffle(series)
	#print(series)
	#print()
	#result = ''.join(l)
	return series


def findOne(n, series):
	global numShuffles 
	global percentFlat
	cross, newbies = intersect(series, n), swap(series, n, 1)
	#print(cross)
	#display(series, n)
	if cross==0: return series
	maxSer = maxVal = n*n+1
	for ser in newbies:
		i = intersect(ser, n)
		if i==0: return ser
		if i < maxVal: maxVal, maxSer = i, ser
		#print (maxVal)
	#print()
	if maxVal>=cross: 
		#print(maxVal, " ", cross)
		if maxVal==cross: percentFlat += 1
		numShuffles += 1
		return findOne(n, randomize(series, n))
	else:
		return findOne(n, maxSer)

def findOne2(n, series, flatVisit):
	global numShuffles2
	cross, newbies = intersect(series, n), swap(series, n, 2)
	if cross==0: return series
	maxSer = maxVal = n*n+1
	for ser in newbies:
		i = intersect(ser, n)
		if i==0: return ser
		if i < maxVal: maxVal, maxSer = i, ser
	if maxVal>cross: 
		numShuffles2 += 1
		return findOne(n, randomize(series, n))
	else:
		if maxVal==cross and maxSer not in flatVisit and not maxSer==n:
			flatVisit.append(maxSer)
			return findOne2(n, maxSer, flatVisit)
		else:
			numShuffles2 += 1
			return findOne2(n, randomize(series, n), [])
		#return findOne2(n, maxSer, [])

def localMin(n, series):
	cross, newbies = intersect(series, n), swap(series, n)
	maxSer = maxVal = cross
	for ser in newbies:
		i = intersect(ser, n)
		if i < cross: maxVal, maxSer = i, ser
	if maxSer == cross:
		print("Local Min:")
		display(series, n)
		print(series, "\n")
	else: return localMin(n, maxSer)

n = int(sys.argv[1])
#order = sys.argv[2]

#listOrd = []
#for num in range(n):
#	listOrd.append(num)

for i in range(15, 16):
	n=i
	print("\n")
	print(n)
	listOrd = []
	for num in range(n):
		listOrd.append(num)


	#flatVisit = set([])
	flatVisit = []
	numLoops = 1
	for i in range(numLoops):
		listOrd = randomize(listOrd, n)
		finalSeries = findOne(n, listOrd)
	for i in range(numLoops):
		listOrd = randomize(listOrd, n)
		finalSeries = findOne2(n, listOrd, flatVisit)
	averageShuff = (numShuffles)/numLoops
	averageSwaps = (numSwaps)/numLoops
	averagePerc = (percentFlat)/numLoops
	averageShuff2 = (numShuffles2)/numLoops
	averageSwaps2 = (numSwaps2)/numLoops
	print("shuffle:", averageShuff)
	print("swaps: ", averageSwaps)
	if averageShuff==0: averageShuff=1
	print("percents: ", averagePerc/averageShuff*100)
	print("percents: ", averagePerc)
	print("shuffle2: ", averageShuff2)
	print("swaps2: ", averageSwaps2)

'''print("\nStarting Board:")
display (listOrd, n)
print(listOrd, "\n")

print("One Solution")
if intersect(listOrd, n)==0:
	display(listOrd, n)
	print(listOrd, "\n")
else:
	finalSeries = findOne2(n, listOrd, set([]))
	display(finalSeries, n)
	print(finalSeries, "\n")'''

#localMin(n, order)


'''def findOne(n, series):
	cross, newbies = intersect(series, n), swap(series, n)
	maxSer = maxVal = cross
	for ser in newbies:
		i = intersect(ser, n)
		if i==0: return ser
		if i < maxVal: maxVal, maxSer = i, ser
	if maxSer==cross: return findOne(n, randomize(series, n))
	else: return findOne(n, maxSer)'''



'''def findOne(n, series):
	print(series)
	global percentFlat
	global numShuffles
	cross, newbies = intersect(series, n), swap(series, n, 1)
	maxSer = maxVal = cross
	for ser in newbies:
		i = intersect(ser, n)
		if i==0: return ser
		if i < maxVal: maxVal, maxSer = i, ser
	if maxSer==cross:
		if maxVal == cross: percentFlat += 1
		numShuffles += 1
		return findOne(n, randomize(series, n))
	else: return findOne(n, maxSer)'''