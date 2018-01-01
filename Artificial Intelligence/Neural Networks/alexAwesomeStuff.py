print("hi im alex. im the best!")

probDict={1:0, 0:1}
def calc(x, w, b):
	#(x1, x2) = x 
	return (1/(1*Decimal(math.e) ** (Decimal(-w*x+b))))
def calcError(diction, w, b):
	sumError = 0
	for p in diction:
		n = sigCalc(p, w, b)
		error = diction[p] - n
		sumError += error**2
	return sumError
def hillClimbing(diction, w, b):
	new = []
	for i in range(-1, 2):
		for j in range(-1, 2):
			wC,bC = w,b
			wC = wC + 7*i
			bC = bC + 7*j 
			new.append((wC, bC))
	modified = False
	minEq, minError = 0, calcError(diction, w, b)
	for piece in new:
		(wA, bA) = piece
		calcError(diction, wA, bA)


