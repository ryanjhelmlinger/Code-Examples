import sys, time

guesses = 0

syms = set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])

groups = []

for x in range(0,9):
	nums = set([])
	for y in range(0,9):
		nums.add(x*9+y)
	groups.append(nums)


for x in range(0,9):
	nums = set([])
	for y in range(0,9):
		nums.add(x+9*y)
	groups.append(nums)
x = 0
while x<61:
	nums = set([])
	y = 0
	while y<21:
		nums.add(x+y)
		if(y==2 or y==11):
			y += 6
		y += 1
	groups.append(nums)
	if x==6 or x==33:
		x += 18
	x += 3

cellNeighbors = []
for cell in range(0, 81):
	indices = set([])
	for sets in groups:
		if cell in sets:
			indices.update(sets)
	indices.remove(cell)
	cellNeighbors.append(indices)

possibilities = {}


def bruteForce(puzzle):
	global possibilities, guesses
	puzzle = deduction(puzzle)
	if len(possibilities) == 0:
		return puzzle
	minIndex = -1
	minVal = 81
	for key in possibilities:
		if len(possibilities[key]) < minVal:
			minIndex = key
			minVal = len(possibilities[key])
	for num in possibilities[minIndex]:
		if not minVal == 1:
			guesses += 1
		updatePossible(puzzle, minIndex, str(num))
		bf = bruteForce(puzzle[:minIndex] + str(num) + puzzle[minIndex+1:])
		if(bf!=""):
			return bf
		else:
			findPossible(puzzle)
	return ""

def deduction(puzzle):
	global possibilities, groups
	for group in groups:
		amount = {}
		for index in group:
			if puzzle[index] == ".":
				for num in possibilities[index]:	
					if num in amount:
						amount[num] = -1
					else:
						amount[num] = index
		for key in amount:
			if amount[key] != -1:
				updatePossible(puzzle, amount[key], key)
				return deduction(puzzle[:amount[key]] + key + puzzle[amount[key]+1:])
	return puzzle

def findPossible(puzzle):
	global possibilities, syms, cellNeighbors
	possibilities = {}
	count = 0
	for char in puzzle:
		if char == ".":
			poss = set([])
			for index in cellNeighbors[count]:
				if puzzle[index] != ".":
					poss.add(puzzle[index])
			possibilities[count] = syms - poss
		count += 1


def updatePossible(puzzle, index, num):
	global cellNeighbors, possibilities
	del possibilities[index]
	for cell in cellNeighbors[index]:
		if cell in possibilities:
			if str(num) in possibilities[cell]:
				possibilities[cell].remove(str(num))



def showBoard(puzzle):
	for x in range(0,9):
		print (puzzle[x*9+0], "", puzzle[x*9+1], "", puzzle[x*9+2], "|", puzzle[x*9+3], "", puzzle[x*9+4], "", puzzle[x*9+5], "|", puzzle[x*9+6], "", puzzle[x*9+7], "", puzzle[x*9+8])
		if x == 2 or x==5:
			print ("---------------------------")

def validateSudoku(puzzle):
	global groups
	for lists in groups:
		temp = set([])
		for pos in lists:
			if puzzle[pos] != ".":
				if puzzle[pos] not in temp:
					temp.add(puzzle[pos])
				else:
					return False
	return True


f = open("sudoku128.txt", "r")
puzzleList= []
for line in f:
	puzzleList.append(line)
if len(sys.argv)>2:
	startTime = time.clock()
	for i in range(int(sys.argv[2])-int(sys.argv[1])+1):
		i += int(sys.argv[1])
		print (i)
		puzzle = puzzleList[i-1]
		print (puzzle,)
		findPossible(puzzle)
		solved = bruteForce(puzzle)
		if(solved == ""):
			print ("INVALID")
		else:
			print (solved)
	print ("\n\n")
	print ("Run time: ", time.clock()-startTime)
	print ("\nGuesses: ", guesses)
elif len(sys.argv)>1:
	startTime = time.clock()
	puzzle = puzzleList[int(sys.argv[1])-1]
	print ("\n")
	showBoard(puzzle)
	print ("\n")
	if validateSudoku(puzzle) == False:
		print ("INVALID")
	else:
		findPossible(puzzle)
		solved = bruteForce(puzzle)
		showBoard(solved)
	print ("\n")
	print ("Run time: ", time.clock()-startTime)
	print ("\nGuesses: ", guesses)
else:
	count = 1
	st = time.clock()
	for puzzle in puzzleList:
		#print (count)
		count += 1
		startTime = time.clock()
		findPossible(puzzle)
		solved = bruteForce(puzzle)
		#if(solved == ""):
		#	print (puzzle)
		#	print ("INVALID")
		#else:
		#	print (puzzle, solved)
		#print ("Run time: ", time.clock()-startTime, "\n\n")
		#print (count-1, ", ", time.clock()-startTime)
	print ("\n")
	print ("\nGuesses: ", guesses)
	print ("Total run time: ", time.clock()-st, "\n\n")


















'''def deductionBlocks(puzzle):
	poss = findPossible(puzzle)
	global blocks
	for i in range(0,9):
		amount = {}
		for index in blocks[i]:
			if puzzle[index] == ".":
				for num in poss[index]:
					if num in amount:
						amount[num] = -1
					else:
						amount[num] = index
		for key in amount:
			if amount[key] != -1:
				return deductionBlocks(puzzle[:amount[key]] + key + puzzle[amount[key]+1:])
	return puzzle

def deductionHorizontals(puzzle):
	poss = findPossible(puzzle)
	global horizontals
	for i in range(0,9):
		amount = {}
		for index in horizontals[i]:
			if puzzle[index] == ".":
				for num in poss[index]:
					if num in amount:
						amount[num] = -1
					else:
						amount[num] = index
		for key in amount:
			if amount[key] != -1:
				return deductionHorizontals(puzzle[:amount[key]] + key + puzzle[amount[key]+1:])
	return puzzle



def deductionVerticals(puzzle):
	poss = findPossible(puzzle)
	global verticals
	for i in range(0,9):
		amount = {}
		for index in verticals[i]:
			if puzzle[index] == ".":
				for num in poss[index]:
					if num in amount:
						amount[num] = -1
					else:
						amount[num] = index
		for key in amount:
			if amount[key] != -1:
				return deductionVerticals(puzzle[:amount[key]] + key + puzzle[amount[key]+1:])
	return puzzle'''


'''prevPuzzle = ""
	while puzzle != prevPuzzle:
		prevPuzzle = puzzle
		puzzle = deductionBlocks(puzzle)
		puzzle = deductionHorizontals(puzzle)
		puzzle = deductionVerticals(puzzle)'''


'''def deduction2(puzzle):
	global syms
	for i in range(0,81):
		if puzzle[i] == ".":
			poss = set([])
			for index in cellNeighbors[i]:
				if puzzle[index] != ".":
					poss.add(puzzle[index])
					poss2 = syms - poss
			if len(poss2) == 1:
				#print ("here")
				return deduction(puzzle[:i] + poss2.pop() + puzzle[i+1:])
	return puzzle'''


'''def bruteForce(puzzle):
	possList = findPossible(puzzle)
	minIndex = possList[0]
	if minIndex == -1:
		return puzzle
	for num in syms:
		if num not in possList[1]:
			global guesses
			guesses += 1
			bf = bruteForce(puzzle[:minIndex] + str(num) + puzzle[minIndex+1:])
			if(bf!=""):
				return bf
	return ""

def bruteForced(puzzle):
	puzzle = deduction(puzzle)
	return bruteForce(puzzle)'''



'''def findPossible3(puzzle):
	global cellNeighbors
	possDict = {}
	minIndex = -1
	maxSet = set([])
	for i in range(0,81):
		if puzzle[i] == ".":
			poss = set([])
			for index in cellNeighbors[i]:
				if puzzle[index] != ".":
					poss.add(puzzle[index])
			if len(poss) > len(maxSet):
				minIndex = i
				maxSet = poss
	return [minIndex, maxSet]


def findPossible2(puzzle):
	possDict = {}
	global syms
	global cellNeighbors
	count = 0
	for char in puzzle:
		if char == ".":
			poss = set([])
			for index in cellNeighbors[count]:
				if puzzle[index] != ".":
					poss.add(puzzle[index])
			#if len(poss) == 0:
			#	return False
			possDict[count] = poss
		count += 1
	return possDict'''