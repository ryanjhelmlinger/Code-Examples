crossword = [1, '-', 2, '*', '*', 3, '-', '-', 4, '-', '*', 5, '-', '-', '-', '*', '*', '-', '-', '*', '-', '*', '*', 6, '-', 7, '-', 8, 9, '-', 10, '*', '-', '*', '-', '*', '*', '-', '*', 11, '-', '-', '*', '-', '*', '*', '-', '*', '-', '*', 12, 13, '-', 14, 15, '-', '-', '-', '*', '*', '-', '*', '-', '-', '*', '*', 16, '-', '-', '-', '*', '-', 17, '-', '-', '-', '*', '*', '-', '*', '-']
possDict = {(1,"across"): set(["DAD"]), (3,"across"): set(["SEND"]), 
(5,"across"): set(["EAST"]), (6,"across"): set(["ITSY"]), 
(8,"across"): set(["NERF"]), (11,"across"): set(["ARK"]), 
(12,"across"): set(["SYNC"]), (15,"across"): set(["MESH"]), 
(16,"across"): set(["EVER"]), (17,"across"): set(["NEAR"]), 
(1,"down"): set(["DOWN"]), (2,"down"): set(["DEAR"]), 
(3,"down"): set(["STINKS"]), (4,"down"): set(["DAY"]), 
(7,"down"): set(["STUN"]), (9,"down"): set(["EASE"]), 
(10,"down"): set(["FATHER"]), (13,"down"): set(["YARD"]), 
(14,"down"): set(["CARD"]), (15,"down"): set(["MAN"])}

def display(puzzle):
	for i in range(0,9):
		for j in range(0,9):
			if puzzle[i*9+j]=='*': puzzle[i*9+j]=' '
			print(puzzle[i*9+j], end=" ")
		print()

#creates indexDict, lengthDict, fillPuzzle, hintDict
def setUp(crossword):
	#indexDict and lengthDict
	indexIntersectDict = {}
	for i in range(0,len(crossword)): indexIntersectDict[i] = set([])
	lengthDict = {}
	for i in range(0,len(crossword)):
		spot = crossword[i]
		if spot!="-" and spot!="*":
			if crossword[i-1]=="*" or i%9==0:
				indexIntersectDict[i].add((spot,"across"))
				count = 0
				for x in range(1, 10):
					count+=1
					
					if crossword[i+x]=="*" or (i+x)%9==0 or i+x==9**2-1:
						lengthDict[(spot,"across")] = count
						break
					indexIntersectDict[i+x].add((spot,"across"))
			if crossword[i-9]=="*" or i<9:
				indexIntersectDict[i].add((spot,"down"))
				count = 0
				for x in range(1, 10):
					count+=1
					if crossword[i+x*9]=="*":
						lengthDict[(spot,"down")] = count
						break
					indexIntersectDict[i+x*9].add((spot,"down"))
					if (i+x*9)>9**2-9-1:
						lengthDict[(spot,"down")] = count+1
						break
	#fillPuzzle
	filledPuzzle = []
	for spot in crossword:
		if not (spot=="*" or spot=="-"): filledPuzzle.append("-")
		else: filledPuzzle.append(spot)
	#hintDict
	hintIntersectDict = {}
	for index in indexIntersectDict:
		for numDir in indexIntersectDict[index]:
			if numDir in hintIntersectDict: hintIntersectDict[numDir].add(index)
			else: hintIntersectDict[numDir] = set([index])
	for key in hintIntersectDict:
		hintIntersectDict[key] = sorted(hintIntersectDict[key])

	return (indexIntersectDict,lengthDict,hintIntersectDict,filledPuzzle)

#removes puzzle words of the wrong length
def removeWrongLength(possDict, lengthDict):
	for num in possDict:
		notCorrectLenth = []
		for word in possDict[num]:
			if len(word)!= lengthDict[num]:
				notCorrectLenth.append(word)
		for word in notCorrectLenth:
			possDict[num].remove(word)
	return possDict

#recursive method to fill in crossword puzzle
def solve(filledPuzzle, numDir, level):
	global alreadyUsed, indexDict, hintDict, possDict
	possibility=False
	if '-' not in filledPuzzle: return filledPuzzle
	for word in possDict[numDir]:
		backup = []
		for spot in filledPuzzle: backup.append(spot)
		count = 0
		included = set([])
		for index in hintDict[numDir]:
			if filledPuzzle[index]=='-':
				filledPuzzle[index] = word[count]
				count+=1
				for hint in indexDict[index]: included.add(hint)
			elif filledPuzzle[index]==word[count]: count+=1
			else:
				if filledPuzzle[index]!=word[count]:
					filledPuzzle = []
					for spot in backup: filledPuzzle.append(spot)
					break
		else:
			possibility=True
			for hint in included:
				if hint not in alreadyUsed:
					alreadyUsed.append(hint)
					branchOut = solve(filledPuzzle, hint, level+1)
					if branchOut != False: filledPuzzle = branchOut
					else:
						alreadyUsed.remove((hint))
						filledPuzzle = []
						for spot in backup: filledPuzzle.append(spot)
						break
	if possibility==False: return False
	else: return filledPuzzle



indexDict,lengthDict,hintDict,filledPuzzle = setUp(crossword)
possDict = removeWrongLength(possDict, lengthDict)
alreadyUsed = [(1,"across")]

solution = solve(filledPuzzle, (1,"across"), 1)
if solution!=False: display(solution)
else: print(solution)