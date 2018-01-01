import sys, time, contextlib, msvcrt, math, random
from random import shuffle


def kbfunc():
    x = msvcrt.kbhit()
    if x: ret = msvcrt.getch()
    else: ret = False
    return ret

def showBoard(puzzle):
	top = "-"*26
	print("\n     " + top)
	for x in range(0,8):
		print ("   " + str(x) + " | " + puzzle[x*8+0], "", puzzle[x*8+1], 
			"", puzzle[x*8+2], "", puzzle[x*8+3], "", puzzle[x*8+4], "", 
			puzzle[x*8+5], "", puzzle[x*8+6], "", puzzle[x*8+7] + " | " + str(x))
	print("     " + top + "\n       0  1  2  3  4  5  6  7\n")
	ocount = xcount = 0
	for letter in puzzle:
		if letter == "O": ocount += 1
		if letter == "X": xcount += 1
	print("X: ", xcount)
	print("O: ", ocount, "\n")

def findNeighbors():
	neighbors = {}
	for x in range(0,8):
		for y in range(0,8):
			neighborList = []
			lower, upper = -1, 2
			if y == 0: lower = 0
			if y == 7: upper = 1
			for w in range(-1,2):
				for z in range (lower,upper):
					index = 8*x+y+8*w+z
					if index > 0 and index < 64 and index != 8*x+y:
						neighborList.append(8*x+y+8*w+z)
			neighbors[8*x+y] = neighborList
	return neighbors

def findPossibilities(puzzle, letter):
	possibilities, eligible = set([]), True
	for x in range(0, 64):
		if puzzle[x] == ".":
			for part in neighbors[x]:
				if puzzle[part]!=letter and puzzle[part]!=".":
					difference, count = x-part, 0
					while(-1<part<64 and puzzle[part]!=letter and puzzle[part]!="." and eligible==True):
						count += 1
						part += -difference
						if math.fabs((part+difference)%8-part%8)==7:
							eligible = False
					if not(part<0 or part>63 or puzzle[part]=="." or eligible==False):
						edited = False
						for tup in possibilities:
							loc, num = tup
							if x==loc:
								edited = True
								num += count
								possibilities.remove(tup)
								possibilities.add((x,num))
						if edited == False: possibilities.add((x,count))
					eligible = True
	return possibilities

def inputSpot(puzzle, index, letter):
	mightWork, possibilities, eligible = set([]), set([]), True
	for part in neighbors[index]:
		if puzzle[part]!=letter and puzzle[part]!=".":
			mightWork, difference = set([]), index-part
			mightWork.add(part)
			while(-1<part<64 and puzzle[part]!=letter and puzzle[part]!="." and eligible==True):
				part += -difference
				mightWork.add(part)
				if math.fabs((part+difference)%8-part%8)==7:
					eligible = False
			if not(part<0 or part>63 or puzzle[part]=="." or eligible==False):
				#for node in mightWork: possibilities.add(node)
				for number in mightWork: puzzle = puzzle[:number] + letter + puzzle[number+1:]
				#possibilities.add(index)
			eligible = True
	puzzle = puzzle[:index] + letter + puzzle[index+1:]
	#for number in possibilities: puzzle = puzzle[:number] + letter + puzzle[number+1:]
	return puzzle

def printWinner(puzzle):
	showBoard(puzzle)
	ocount = xcount = 0
	for letter in board:
		if letter == "O": ocount += 1
		if letter == "X": xcount += 1
	if ocount>xcount: print("PLayer O won by a final score of ", ocount, "-", xcount)
	if ocount<xcount: print("PLayer X won by a final score of ", xcount, "-", ocount)
	if ocount==xcount: print("The final result was a tie")

def printWinner2(puzzle):
	ocount = xcount = 0
	for letter in board:
		if letter == "O": ocount += 1
		if letter == "X": xcount += 1
	return [xcount, ocount]


def compVal(board, turnLetter):
	myVal = oppVal = 0
	for ind in range(0, 64):
		if board[ind] == turnLetter:
			myVal += weighting[ind]
		if board[ind] != "." and board[ind] != turnLetter:
			oppVal += weighting[ind]
	return myVal-oppVal


def compChoose4(board, turnLetter):
	possibleMoves = findPossibilities(board, turnLetter)
	maxVal = maxInd = -1000000
	for tup in possibleMoves:
		index, num = tup
		value = compChoose3Helper(inputSpot(board, index, turnLetter), turnLetter)
		#print ("here", value, " ", index, " ", turnLetter)
		if value > maxVal:
			maxInd = index
			maxVal = value
	board = inputSpot(board, maxInd, turnLetter)
	if turnLetter == "O": turnLetter = "X"
	else: turnLetter = "O"
	return [board, turnLetter]

def compChoose3Helper(board, turnLetter, level):
	if level > 0:
		return compVal(board, turnLetter)
	level += 1
	possibleMoves = findPossibilities(board, turnLetter)
	maxVal = maxInd = -1000000
	for tup in possibleMoves:
		index, num = tup
		value = compChoose3Helper(inputSpot(board, index, turnLetter), turnLetter, level)
		if value > maxVal:
			maxInd = index
			maxVal = value
	if maxInd <0:
		return compVal(board, turnLetter)
	board = inputSpot(board, maxInd, turnLetter)
	if turnLetter == "O": turnLetter = "X"
	else: turnLetter = "O"
	return maxVal

def compChoose3(board, turnLetter):
	possibleMoves = findPossibilities(board, turnLetter)
	maxVal = maxInd = -1000000
	for tup in possibleMoves:
		index, num = tup
		value = compChoose3Helper(inputSpot(board, index, turnLetter), turnLetter, 0)
		print("X val is ", compVal(inputSpot(board, index, turnLetter), "X"), " and O val is ", compVal(inputSpot(board, index, turnLetter), "O"))
		showBoard(inputSpot(board, index, turnLetter))
		#print ("here", value, " ", index, " ", turnLetter)
		if value > maxVal:
			maxInd = index
			maxVal = value
	if maxInd <0:
		return compVal(board, turnLetter)
	board = inputSpot(board, maxInd, turnLetter)
	if turnLetter == "O": turnLetter = "X"
	else: turnLetter = "O"
	return [board, turnLetter]

def compChoose2(board, turnLetter):
	possibleMoves = findPossibilities(board, turnLetter)
	index, num = random.choice(list(possibleMoves))
	board = inputSpot(board, index, turnLetter)
	if turnLetter == "O": turnLetter = "X"
	else: turnLetter = "O"
	return [board, turnLetter]

def compChoose(board, turnLetter):
	possibleMoves = findPossibilities(board, turnLetter)
	greatnum = goodnum = neutralnum = badnum = terriblenum = -1
	greatInd = goodInd = neutralInd = badInd = terribleInd = -1
	for tup in possibleMoves:
		loc, num = tup
		if loc in great: 
			if greatnum < num: greatnum, greatInd = num, loc
		if loc in good: 
			if goodnum < num: goodnum, goodInd = num, loc
		if loc in neutral: 
			if neutralnum < num: neutralnum, neutralInd = num, loc
		if loc in bad: 
			if badnum < num: badnum, badInd = num, loc
		if loc in terrible: 
			if terriblenum < num: terriblenum, terribleInd = num, loc
	if greatInd > -1: board = inputSpot(board, greatInd, turnLetter)
	elif goodInd > -1: board = inputSpot(board, goodInd, turnLetter)
	elif neutralInd > -1: board = inputSpot(board, neutralInd, turnLetter)
	elif badInd > -1: board = inputSpot(board, badInd, turnLetter)
	else: board = inputSpot(board, terribleInd, turnLetter)
	if turnLetter == "O": turnLetter = "X"
	else: turnLetter = "O"
	return [board, turnLetter]


def countBoard(puzzle, turnLetter):
	oscore = xscore = count = 0
	for spot in puzzle:
		if spot == "O":
			oscore += weighting[spot]

def flipOrRotate(board, array, turnLetter):
	flipRot = [None]*64
	for i in range(0,64): flipRot[i] = board[array[i]]
	showBoard(flipRot)
	return [board, turnLetter]

def playerTurn(board, turnLetter):
	loc = input("It is player " + turnLetter + "'s turn:  ").lower()
	if loc=="rl": return flipOrRotate(board, rl, turnLetter)
	if loc == "rr": return flipOrRotate(board, rr, turnLetter)
	if loc == "r2": return flipOrRotate(board, r2, turnLetter)
	if loc == "fx": return flipOrRotate(board, fx, turnLetter)
	if loc == "fy": return flipOrRotate(board, fy, turnSLetter)
	if loc == "fd": return flipOrRotate(board, fd, turnLetter)
	if loc == "fo": return flipOrRotate(board, fo, turnLetter)
	if loc == "i":
		showBoard(board)
		return [board, turnLetter]
	if len(loc)==2: index = int(loc)
	else:
		row = col = -1
		for letter in loc:
			if letter in acceptable:
				if row == -1:
					row = int(letter)
				else:
					col = int(letter)
					break
		index = 8*row+col
	possibleMoves, valid = findPossibilities(board, turnLetter), False
	for tup in possibleMoves:
		loc, num = tup
		if index == loc:
			board, valid = inputSpot(board, index, turnLetter), True
			if turnLetter == "O":
				turnLetter = "X"
			else:
				turnLetter = "O"
	if valid == False: print("Move was invalid")
	return [board, turnLetter]

def possPass(board, tl):
	oposs, xposs = findPossibilities(board, "O"), findPossibilities(board, "X")
	if len(xposs)==0:
		if len(oposs)==0: return "*"
		else: tl = "O"
	if len(oposs)==0: tl = "X"
	return tl

neighbors = findNeighbors()

rl = [7, 15, 23, 31, 39, 47, 55, 63, 6, 14, 22, 30, 38, 46, 54, 62, 5, 13, 21, 29, 37, 45, 53, 61, 4, 12, 20, 28, 36, 44, 52, 60, 3, 11, 19, 27, 35, 43, 51, 59, 2, 10, 18, 26, 34, 42, 50, 58, 1, 9, 17, 25, 33, 41, 49, 57, 0, 8, 16, 24, 32, 40, 48, 56]
rr = [56, 48, 40, 32, 24, 16, 8, 0, 57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 28, 20, 12, 4, 61, 53, 45, 37, 29, 21, 13, 5, 62, 54, 46, 38, 30, 22, 14, 6, 63, 55, 47, 39, 31, 23, 15, 7]
r2 = [63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
fx = [7, 6, 5, 4, 3, 2, 1, 0, 51, 41, 31, 21, 11, 10, 9, 8, 23, 22, 21, 20, 19, 18, 17, 16, 31, 30, 29, 28, 27, 26, 25, 24, 39, 38, 37, 36, 35, 34, 33, 32, 47, 46, 45, 44, 43, 42, 41, 40, 55, 54, 53, 52, 51, 50, 49, 48, 63, 62, 61, 60, 59, 58, 57, 56]
fy = [56, 57, 58, 59, 60, 61, 62, 63, 48, 49, 50, 51, 52, 53, 54, 55, 40, 41, 42, 43, 44, 45, 46, 47, 32, 33, 34, 35, 36, 37, 38, 39, 24, 25, 26, 27, 28, 29, 30, 31, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7]
fd = [63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 60, 52, 44, 36, 28, 20, 12, 4, 59, 51, 43, 35, 27, 19, 11, 3, 58, 50, 42, 34, 26, 18, 10, 2, 57, 49, 41, 33, 25, 17, 9, 1, 56, 48, 40, 32, 24, 16, 8, 0]
fo = [0, 8, 16, 24, 32, 40, 48, 56, 1, 9, 17, 25, 33, 41, 49, 57, 2, 10, 18, 26, 34, 42, 50, 58, 3, 11, 19, 27, 35, 43, 51, 59, 4, 12, 20, 28, 36, 44, 52, 60, 5, 13, 21, 29, 37, 45, 53, 61, 6, 14, 22, 30, 38, 46, 54, 62, 7, 15, 23, 31, 39, 47, 55, 63]

great = set([0, 7, 56, 63])
good = set([2, 3, 4, 5, 16, 24, 32, 40, 23, 31, 39, 47, 58, 59, 60, 61])
neutral = set([18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37, 42, 43, 44, 45])
bad = set([10, 11, 12, 13, 17, 25, 33, 41, 22, 30, 38, 46, 50, 51, 52, 53])
terrible = set([1, 6, 8, 14, 48, 55, 57, 62, 9, 15, 49, 54])

weighting = {}
for index in great: weighting[index] = 20
for index in good: weighting[index] = 10
for index in neutral: weighting[index] = 5
for index in bad: weighting[index] = 2
for index in terrible: weighting[index] = 1

#print(weighting)

acceptable = set(["0", "1", "2", "3", "4", "5", "6", "7"])
board = "...........................OX......XO..........................."
turnLetter = "X"
first = sys.argv[1].lower()
second = sys.argv[2].lower()
third = 0
if len(sys.argv)>3:
	third = sys.argv[3]

if first == "p" and second == "c":
	while True:
		showBoard(board)
		turnLetter = possPass(board, turnLetter)
		if turnLetter == "*": break
		if turnLetter == "X": board, turnLetter = playerTurn(board, turnLetter)
		else: board, turnLetter = compChoose(board, turnLetter)
	printWinner(board)
elif first == "p" and second == "p":
	while True:
		showBoard(board)
		turnLetter = possPass(board, turnLetter)
		if turnLetter == "*": break
		board, turnLetter = playerTurn(board, turnLetter) 
	printWinner(board)
elif first == "c" and second == "p":
	while True:
		showBoard(board)
		turnLetter = possPass(board, turnLetter)
		if turnLetter == "*": break
		if turnLetter == "O": board, turnLetter = playerTurn(board, turnLetter)
		else: board, turnLetter = compChoose(board, turnLetter)
	printWinner(board)
elif first=="c" and second=="c" and third==0:
	while True:
		showBoard(board)
		turnLetter = possPass(board, turnLetter)
		if turnLetter == "*": break
		if turnLetter == "X": board, turnLetter = compChoose3(board, turnLetter)
		else: board, turnLetter = compChoose2(board, turnLetter)
		#print("X val is ", compVal(board, "X"), " and O val is ", compVal(board, "O"))
		print("It is player " + turnLetter + "'s turn:  ")
else:
	st = time.clock()
	lastTurn = "X"
	xcount = ocount = xwin = owin = twin = count = 0
	for i in range(0, int(third)):
		while(True):
			#showBoard(board)
			turnLetter = possPass(board, turnLetter)
			if turnLetter == "*": break
			if turnLetter == "X": board, turnLetter = compChoose3(board, turnLetter)
			else: board, turnLetter = compChoose2(board, turnLetter)
		x, o = printWinner2(board)
		xcount += x
		ocount += o
		if x>o: xwin += 1
		elif x<o: owin += 1
		else: twin += 1
		if lastTurn == "X": turnLetter, lastTurn = "O", "O"
		else: turnLetter, lastTurn = "X", "X"
		board = "...........................OX......XO..........................."
	print("\nPlayer X won ", xwin, " times, player O won ", owin, " times, and there were ", twin, " ties.")
	print("\nThe total flipped were X: ", xcount, "and O: ", ocount)
	print("\n\n took a total of ", time.clock()-st, " seconds.")
