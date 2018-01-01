import math, sys, random, decimal, copy
from decimal import Decimal, localcontext

def sigCalc(x):
	return 1/(1+Decimal(math.e)**Decimal(-x))

def calcError(rules, weights): 
	bias = 1
	totalError = 0 
	for part in rules:
		(x1,x2) = part
		h1 = x1*weights[0] + x2*weights[2] + bias*weights[4]
		h2 = x1*weights[1] + x2*weights[3] + bias*weights[5]
		h1 = sigCalc(h1)
		h2 = sigCalc(h2)
		y = Decimal(h1)*Decimal(weights[6]) + Decimal(h2)*Decimal(weights[7])
		y = sigCalc(y)
		#num = sigCalc(part, w, b) 
		error = rules[part]-y 
		#print(part, ":  ", y)
		totalError += error**2 
	return totalError 

def hillClimb(rules, weights):
	count=-1
	while True:
		count+=1
		diff, newbies = 10**count, [] 
		minEQ, minError = 0, calcError(rules, weights) 
		edited = False
		for a in range(-1,2): 
			for b in range(-1,2):
				for c in range(-1,2):
					for d in range(-1,2):
						for e in range(-1,2):
							for f in range(-1,2):
								for g in range(-1,2):
									for h in range(-1,2):
										if not a+b+c+d+e+f+g+h==0:
											weights2 = [weights[0]+diff*a, weights[1]+diff*b, weights[2]+diff*c, weights[3]+diff*d, weights[4]+diff*e, weights[5]+diff*f, weights[6]+diff*g, weights[7]+diff*h]
											error = calcError(rules, weights2) 
											if error<minError: 
												edited = True 
												minError = error 
												minEQ = weights2[:]
											#newbies.append(weights2)
		#if minError < .0005:
		#	return (w,b)
		'''for eq in newbies: 
			weights2 = eq
			error = calcError(rules, weights2) 
			if error<minError: 
				edited = True 
				minError = error 
				minEQ = eq'''
		#print(minError)
		#print(minEQ)
		#print(edited)
		#print()

		if edited == True:
			weights = minEQ
			continue
		else: return weights


#probDict = {1:0, 0:1}                    #NOT
#probDict = {(0,0):0, (1,0):0, (1,1):1}	  #AND
#probDict = {(0,0):0, (1,0):1, (1,1):1}	  #OR
probDict = {(0,0):0, (1,0):1, (0,1):1, (1,1):0}    #XOR
weights = []
#inputOne = sys.argv[1]
#inputTwo = sys.argv[2]


minOverError = float('inf')	
while True: 
	weights = []
	for i in range(0,8):
		weights.append(int(random.uniform(-10,10)))
	weights=hillClimb(probDict, weights)
	error = calcError(probDict, weights)
	if error<minOverError: 
		print()
		minOverError = error
		print()
		print("Weights: ", weights)
		print("Error: ", error) 
		if error==0: break