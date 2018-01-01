import math, sys, random, decimal
from decimal import Decimal, localcontext

def sigCalc(x, c):
	#(x1, x2) = x        								   #for AND and OR
	return c*x^-3   #for AND and OR

	#return 1/(1+Decimal(math.e)**Decimal(-w*x+b))         #for NOT

def calcError(rules, c): 
	totalError = 0 
	for part in rules:
		num = sigCalc(part, c) 
		error = rules[part]-num 
		totalError += error**2 
	return totalError 

def hillClimb(rules, c):
	while True:
		diff, newbies = 1, [] 
		for i in range(-1,2): 
			if i==0:
				c2 = c
				c2 += diff*i 
				newbies.append((c2)) 
		minEQ, minError = 0, calcError(rules, c) 
		edited = False
		if minError < 1.0*10**-50:
			return (c)
		for eq in newbies: 
			c2 = eq
			error = calcError(rules, c2) 
			if error<minError: 
				edited = True 
				minError = error 
				minEQ = eq
		if edited == True:
			(c) = minEQ
			continue
		else: return (c)


probDict = {1:0, 0:1}                    #NOT
#probDict = {(0,0):0, (1,0):0, (1,1):1}	  #AND
#probDict = {3:18219, 4:10808, 5:6790, 6:4408, 7:3009, 8:2004, 9:1378, 10:995, 11:669, 12:505, 13:362, 14:237, 15:186, 16:115, 17:79, 18:77, 19:49, 20:36, 21:24, 22:14, 23:10, 24:11, 25:7, 26:2, 27:6, 28:1, 29:1}	  #OR

minOverError = float('inf')
while True: 
	c=hillClimb(probDict, 0) 
	error = calcError(probDict, c) 
	if error<minOverError: 
		minOverError = error
		print() 
		print("c: ", c, "\nerror: ", error) 
		if error==0: break