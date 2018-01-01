import sys, copy, time, random
from random import randint

offSpring = 0
minInters = 1000000000
costTime = 0

def display(board, n):
	for r in range(0,n):
		c = board[r]
		for col in range(0,n):
			if not col==c: print("-", end=' ')
			else: print("*", end=' ')
		print("")

'''def cost(series, n):
	intersects = {}
	for r in range(n):
		c1 = c2 = c = series[r]
		while r >= 0:
			r -= 1
			c1 -= 1
			c2 += 1
		while r <= n-1:
			if series[r]==c1 and not c1==c2:
				if r*n+c1 in intersects: intersects[r*n+c1] += 1
				else: intersects[r*n+c1] = 1
			if series[r]==c2 and not c1==c2:
				if r*n+c2 in intersects: intersects[r*n+c2] += 1
				else: intersects[r*n+c2] = 1
			if series[r]==c and not c1==c2:
				if r*n+c in intersects: intersects[r*n+c] += 1
				else: intersects[r*n+c] = 1
			c1 += 1
			c2 -= 1
			r += 1
	maxIntersect = 0
	for key in intersects: 
		maxIntersect += intersects[key]
		print(int(key/4)+1, ",", key%4, ": ", intersects[key])
	return maxIntersect'''


def cost2(series, size):
	startTime = time.clock()
	intersects = {}
	for r in range(size):
		row = r
		col = c1 = c2 = series[row]
		while row>0:
			row = row-1
			c1 = c1-1
			c2 = c2+1
		while row<n:
			if series[row]==c1 and not c1==c2:
				if row*n+c1 in intersects: intersects[row*n+c1]+=1
				else: intersects[row*n+c1]=1
			if series[row]==c2 and not c1==c2:
				if row*n+c2 in intersects: intersects[row*n+c2]+=1
				else: intersects[row*n+c2]=1
			if series[row]==col:
				if row*n+col in intersects: intersects[row*n+col]+=1
				else: intersects[row*n+col]=1
			row+=1
			c1+=1
			c2 = c2-1
	maxIntersects = 0
	for key in intersects:
		#if intersects[key]>maxIntersects:
		maxIntersects += intersects[key]
	interTime = time.clock()-startTime
	global costTime
	costTime += interTime
	return maxIntersects

def cost(series, size):
	startTime = time.clock()
	intersects = {}
	for r in range(size):
		row = r
		col = c1 = c2 = series[row]
		while row>0:
			if series[row]==c1 and not c1==c2:
				if row*n+c1 in intersects: intersects[row*n+c1]+=1
				else: intersects[row*n+c1]=1
			if series[row]==c2 and not c1==c2:
				if row*n+c2 in intersects: intersects[row*n+c2]+=1
				else: intersects[row*n+c2]=1
			if series[row]==col:
				if row*n+col in intersects: intersects[row*n+col]+=1
				else: intersects[row*n+col]=1
			row = row-1
			c1 = c1-1
			c2 = c2+1
		row = r
		col = c1 = c2 = series[row]
		while row<n-1:
			row+=1
			c1+=1
			c2 = c2-1
			if series[row]==c1 and not c1==c2:
				if row*n+c1 in intersects: intersects[row*n+c1]+=1
				else: intersects[row*n+c1]=1
			if series[row]==c2 and not c1==c2:
				if row*n+c2 in intersects: intersects[row*n+c2]+=1
				else: intersects[row*n+c2]=1
			if series[row]==col:
				if row*n+col in intersects: intersects[row*n+col]+=1
				else: intersects[row*n+col]=1
	maxIntersects = 0
	for key in intersects:
		#if intersects[key]>maxIntersects:
		maxIntersects += intersects[key]
	interTime = time.clock()-startTime
	global costTime
	costTime += interTime
	return maxIntersects


def combine(padre, madre, size, population):
	global offSpring
	offSpring += 1
	par1, ignore = padre
	par2, ignore2 = madre
	split = randint(int(size-size*.75), int(size-size*.25))
	child = par1[:split] + par2[split:]
	if randint(0,8)==0:
		one = randint(0,size-1)
		two = randint(0,size-1)
		temp = child[one]
		child[one] = child[two]
		child[two] = temp
	i = cost(child, size)
	#if i<ignore and i<ignore2:
	#	print(ignore, " ", ignore2, " ", cost(child, size))
	#else:
	#	print("bad")
	for person,i in population:
		if population == person:
			return combine(padre, madre, size, population)
	return (child, cost(child, size))

def nextGeneration(population, size, pool, mini):
	parents = []
	for order,cross in population:
		if randint(0,cross-mini)==0:
			parents.append((order,cross))
			#population.remove((order,cross))
	x=1
	#print(len(parents))
	while x<len(parents):
		population.append(combine(parents[x-1], parents[x], size, population))
		x+=2
	while len(population)>pool:
		#print(len(population))
		minInt = 0
		badpath = 0
		for order,cross in population:
			if cross>minInt:
				badpath = order
				minInt = cross
		population.remove((badpath,minInt))

		#for order,cross in population:
		#	if randint(0,size*size-cross+mini+1)==0: population.remove((order,cross))
		#print(len(population))
		#print("\n")
	while len(population)<pool:
		array = random.sample(range(n),n)
		population.append((array,cost(array,n)))
	return population

n = int(sys.argv[1])
popSize = int(n/2)
#popSize = 2


population = []

for i in range(0,popSize):
	array = random.sample(range(n),n)
	population.append((array,cost(array,n)))

found = False
startTime = time.clock()
count=0
while(True):
	count+=1
	minNum=n*n*n
	for person,cross in population:
		if cross<minNum: minNum=cross
		if cross==n: found, order = True, person
	if minNum<minInters:
		minInters=minNum
		print(minInters)
	if found == True: break
	else: population = nextGeneration(population, n, popSize, minNum)

	
print(order)
print(count)
display(order,n)
print ("Run time: ", time.clock()-startTime)
print(offSpring)
print(costTime)


'''#array = random.sample(range(n),n)
array = [randint(0,4), randint(0,4), randint(0,4), randint(0,4)]
display(array, n)
print("\n")
i = cost(array, n)
print(i)'''
















