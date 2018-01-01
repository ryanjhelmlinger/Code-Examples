import sys, urllib, time, queue
from math import pi , acos , sin , cos

#Read in the soduko puzzles from sudoku128.txt
#showBoard(puzzle)
#validateSudoko(puzzle)
guesses = 0

def bruteForce(puzzle):
	if not validateSudoku(puzzle):
		return ""
	pos = puzzle.find('.')
	if pos<0:
		return puzzle
	for c in "123456789":
		global guesses
		guesses += 1
		bf = bruteForce(puzzle[:pos] + c + puzzle[pos+1:])
		if(bf!=""):
			return bf
	return ""

def bruteForce2(puzzle):
	#if not validateSudoku(puzzle):
	#	return ""
	pos = puzzle.find('.')
	if pos<0:
		return puzzle
	for c in "123456789":
		if validateSpot(puzzle, pos, c):
			global guesses
			guesses += 1
			bf = bruteForce2(puzzle[:pos] + c + puzzle[pos+1:])
			if(bf!=""):
				return bf
	return ""


def bruteForce3(puzzle):
	#if not validateSudoku(puzzle):
	#	return ""

	pos = puzzle.find('.')
	if pos<0:
		return puzzle

	count=0
	indexMin = -1
	setLengthMin = sys.maxint
	setMin = set([])
	for num in puzzle:
		if num == ".":
			currSet = possibleSets(puzzle, count)
			if len(currSet) < setLengthMin:
				indexMin = count
				setLengthMin = len(currSet)
				setMin = currSet
		count += 1


	for number in setMin:
		global guesses
		guesses += 1
		bf = bruteForce(puzzle[:indexMin] + str(number) + puzzle[indexMin+1:])
		if(bf!=""):
			return bf
	return ""


def showBoard(puzzle):
	x = 0
	while x<9:
		print (puzzle[x*9+0], "", puzzle[x*9+1], "", puzzle[x*9+2], "|", puzzle[x*9+3], "", puzzle[x*9+4], "", puzzle[x*9+5], "|", puzzle[x*9+6], "", puzzle[x*9+7], "", puzzle[x*9+8])
		if x == 2 or x==5:
			print ("---------------------------")
		x += 1


def possibleSets(puzzle, index):
	possibleSet = set([1,2,3,4,5,6,7,8,9])
	x=0
	while x<9:
		if index>=x*9 and index<(x+1)*9:
			y=x*9
			while y<(x+1)*9:
				if puzzle[y] in possibleSet:
					possibleSet.remove(puzzle[y])
				y += 1
		x += 1

	x=0
	while x<9:
		if index==x or index==x+9 or index==x+18 or index==x+27 or index==x+36 or index==x+45 or index==x+54 or index==x+63 or index==x+72:
			y=0
			while y<9:
				if puzzle[x+y*9] in possibleSet:
					possibleSet.remove(puzzle[x+y*9])
				y += 1
		x += 1

	x=0
	while x<60:
		if index==x or index==x+1 or index==x+2 or index==x+9 or index==x+10 or index==x+11 or index==x+18 or index==x+19 or index==x+20:
			y=0
			while y<27:
				z=0
				while z<3:
					if puzzle[x+y+z] in possibleSet:
						possibleSet.remove(puzzle[x+y+z])
					z += 1
				y += 9
		if x==6 or x==33:
			x += 21
		else:
			x += 3
	return possibleSet


def validateSpot(puzzle, index, number):
	x=0
	while x<9:
		if index>=x*9 and index<(x+1)*9:
			y=x*9
			while y<(x+1)*9:
				if puzzle[y] == number:
					return False
				y += 1
		x += 1

	x=0
	while x<9:
		if index==x or index==x+9 or index==x+18 or index==x+27 or index==x+36 or index==x+45 or index==x+54 or index==x+63 or index==x+72:
			y=0
			while y<9:
				if puzzle[x+y*9] == number:
					return False
				y += 1
		x += 1

	x=0
	while x<60:
		if index==x or index==x+1 or index==x+2 or index==x+9 or index==x+10 or index==x+11 or index==x+18 or index==x+19 or index==x+20:
			y=0
			while y<27:
				z=0
				while z<3:
					if puzzle[x+y+z] == number:
						return False
					z += 1
				y += 9
		if x==6 or x==33:
			x += 21
		else:
			x += 3
	return True


def validateSudoku(puzzle):
	x = 0
	while x<81:
		nums = set([])
		y = 0
		while y<9:
			if puzzle[x+y] in nums:
				#print nums
				#print puzzle[x+y], " ", x, " ", y
				return False
			else:
				if puzzle[x+y] != ".":
					nums.add(puzzle[x+y])
			y += 1
		x += 9
	x = 0
	while x<9:
		nums = set([])
		y = 0
		while y<9:
			if puzzle[x+9*y] in nums:
				#print puzzle[x+9*y], ", ", x, ", ", y
				return False
			else:
				if puzzle[x+9*y] != ".":
					nums.add(puzzle[x+9*y])
			y += 1
		x += 1
	x = 0
	while x<60:
		nums = set([])
		y = 0
		while y<21:
			if puzzle[x+y] in nums:
				#print puzzle[x+y], ", ", x, " ", y
				return False
			else:
				if puzzle[x+y] != ".":
					nums.add(puzzle[x+y])
			if(y==2 or y==11):
				y += 7
			else:
				y += 1
		if x==6 or x==33:
			x += 21
		else:
			x += 3
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
		puzzle = puzzleList[i]
		#showBoard(puzzle)
		print (puzzle,)
		solved = bruteForce2(puzzle)
		#showBoard(solved)
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
	#puzzle = "11..............................................................................."
	print ("\n")
	showBoard(puzzle)
	print ("\n")
	if validateSudoku(puzzle) == False:
		print ("INVALID")
	else:
		solved = bruteForce2(puzzle)
	#if(solved == ""):
	#		print "INVALID"
	#else:
		#print solved
		showBoard(solved)
	print ("\n")
	print ("Run time: ", time.clock()-startTime)
	print ("\nGuesses: ", guesses)
else:
	count = 1
	st = time.clock()
	for puzzle in puzzleList:
		print (count)
		count += 1
		startTime = time.clock()
		print (puzzle,)
		solved = bruteForce2(puzzle)
		if(solved == ""):
			print ("INVALID")
		else:
			print (solved)
		print ("Run time: ", time.clock()-startTime, "\n\n")
	print ("\n")
	print ("\nGuesses: ", guesses)
	print ("Total run time: ", time.clock()-st, "\n\n")