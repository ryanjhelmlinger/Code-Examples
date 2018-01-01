import sys, copy, time, random
from random import randint

def display(board, n):
	for r in range(0,n):
		c = board[r]
		for col in range(0,n):
			if not col==c: print("-", end=' ')
			else: print("*", end=' ')
		print("")

def cost(series, n):
	intersects = {}
	for r in range(n):
		c1 = c2 = c = series[r]
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
			if series[r]==c and not c1==c2:
				if r*n+c in intersects: intersects[r*n+c] += 1
				else: intersects[r*n+c] = 1
			c1 += 1
			c2 -= 1
			r += 1
	maxIntersect = 0
	for key in intersects: maxIntersect += intersects[key]
	return maxIntersect


n = int(sys.argv[1])

while(True):
	array = random.sample(range(n),n)
	if cost(array,n) == 0: break

display(array,n)