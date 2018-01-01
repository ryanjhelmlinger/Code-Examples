import sys, copy, time
#from copy import copy, deepcopy


def display(board, n):
	for r in range(n):
		for c in range(n):
			if board[r*n+c]==2: board = board[:r*n+c]+"-"+board[r*n+c+1:]
			else: board[:r*n+c]+"*"+board[r*n+c+1:]
			print (board[r*n+c], end=' ')
		print("")

def display2(board, n):
	for r in range(n):
		for c in range(n):
			if board[r*n+c]=="2": board = board[:r*n+c]+"-"+board[r*n+c+1:]
			else: board = board[:r*n+c]+"*"+board[r*n+c+1:]
			print (board[r*n+c], end=' ')
		print("")

def fillDiags(board, r, c, n):
	c1 = c2 = c
	while r > 0:
		r -= 1
		c1 -= 1
		c2 += 1
	while r < n:
		if c1>=0 and c1<n and board[r][c1] == 0: board[r][c1] = 2
		if c2>=0 and c2<n and board[r][c2] == 0: board[r][c2] = 2
		c1 += 1
		c2 -= 1
		r += 1
	return board

def fillDiags2(board, r, c, n):
	c1 = c2 = c
	while r > 0:
		r -= 1
		c1 -= 1
		c2 += 1
	while r < n:
		if c1>=0 and c1<n and board[r*n+c1] == "0": board = board[:r*n+c1]+"2"+board[r*n+c1+1:]
		if c2>=0 and c2<n and board[r*n+c2] == "0": board = board[:r*n+c2]+"2"+board[r*n+c2+1:]
		c1 += 1
		c2 -= 1
		r += 1
	return board

def fillLines(board, r, c, n):
	row, col = r, c
	while r >= 0: r -= 1
	while r < n:
		if board[r][col]==0: board[r][col]=2
		r+=1
	while c >= 0: c -= 1
	while c < n:
		if board[row][c]==0: board[row][c]=2
		c+=1
	return board

def fillLines2(board, r, c, n):
	row, col = r, c
	while r > 0: r -= 1
	while r < n:
		if board[r*n+col]=="0": board = board[:r*n+c]+"2"+board[r*n+c+1:]
		r+=1
	while c > 0: c -= 1
	while c < n:
		if board[row*n+c]=="0": board = board[:r*n+c]+"2"+board[r*n+c+1:]
		c+=1
	return board

def checkIfWon(board, n):
	count = 0
	for r in range(n): 
		for c in range(n): 
			if board[r][c] == 1:
				count += 1
				break
	if count == n: return True
	else: return False

def checkIfWon2(board, n):
	count = 0
	for r in range(n): 
		for c in range(n): 
			if board[r*n+c] == "1":
				count += 1
				break
	if count == n: return True
	else: return False

def recurPerms(board, n, level):
	level += 1
	toBeReturned = []
	if level==n:
		if checkIfWon(board, n)==True: toBeReturned.append(board)
		return toBeReturned
	full = True
	for c in range(n):
		if board[level][c]==0:
			full = False
			newBoard = deepcopy(board)
			newBoard[level][c] = 1
			newBoard = fillDiags(newBoard, level, c, n)
			newBoard = fillLines(newBoard, level, c, n)
			newList = recurPerms(newBoard, n, level)
			for perm in newList:
				if perm not in toBeReturned: toBeReturned.append(perm)
	if full == True:
		if checkIfWon(board, n)==True: toBeReturned.append(board)
	return toBeReturned

def recurPerms2(board, n, level):
	level += 1
	toBeReturned = set([])
	if level==n:
		if checkIfWon2(board, n)==True: toBeReturned.add(board)
		return toBeReturned
	full = True
	for c in range(n):
		if board[level*n+c]=="0":
			full = False
			newBoard = board
			newBoard = newBoard[:level*n+c]+"1"+newBoard[level*n+c+1:]
			newBoard = fillDiags2(newBoard, level, c, n)
			newBoard = fillLines2(newBoard, level, c, n)
			newList = recurPerms2(newBoard, n, level)
			for perm in newList:
				toBeReturned.add(perm)
	if full == True:
		if checkIfWon2(board, n)==True: toBeReturned.add(board)
	return toBeReturned



n = int(sys.argv[1])
#board = [[0 for x in range(n)] for y in range(n)]
board = "0"*n*n

startTime = time.clock()
#finalSet = recurPerms(board, n, -1)
finalSet = recurPerms2(board, n, -1)
if n < 7:
	for perm in finalSet:
		print("\n")
		display(perm, n)
		display2(perm, n)
print("")
print (len(finalSet))
print ("Run time: ", time.clock()-startTime)


'''def recurPerms(board, n, level):
	level += 1
	toBeReturned = []
	full = True
	for r in range(n):
		for c in range(n):
			newBoard = deepcopy(board)
			char = newBoard[r][c]
			if char==0:
				full = False
				newBoard[r][c] = 1
				newBoard = fillDiags(newBoard, r, c, n)
				newBoard = fillLines(newBoard, r, c, n)
				newList= recurPerms(newBoard, n, level)
				for perm in newList:
					alreadyIn = False
					for solution in toBeReturned:
						if perm==solution:
							alreadyIn = True
					if alreadyIn == False:
						toBeReturned.append(perm)
	if full == True:
		if checkIfWon(board, n)==True:
				toBeReturned.append(board)
	return toBeReturned'''