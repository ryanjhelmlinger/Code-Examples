import sys, time, contextlib, msvcrt


def kbfunc():
    x = msvcrt.kbhit()
    if x:
        ret = msvcrt.getch()
    else:
        ret = False
    return ret

def makeTree(word, dictionary):
	if len(word) > 1:
		firstLetter = word[:1]
		restOfWord = word[1:]
		if firstLetter in dictionary:
			makeTree(restOfWord, dictionary[firstLetter])
		else:
			newDict = {}
			newDict = makeTree(restOfWord, {})
			dictionary[firstLetter] = newDict
			return (dictionary)
	elif len(word) > 0:
		if word not in dictionary:
			dictionary[word] = {}
			return dictionary
		makeTree("", dictionary[word])
	else:
		return {dictionary}
		
wordsTree = {}
f = open("ghost.txt", "r")
wordsList = []
wordsSet = set([])
for line in f:
	wordsSet.add(line.split()[0])
	wordsList.append(line.split()[0])
for word in wordsList:
	makeTree(word, wordsTree)


numPlayers = int(sys.argv[1])
players = {}
for i in range(1, numPlayers+1):
	players[i] = ""

numbers = set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
s = ""
turn = 0
while(True):
	prev = turn
	while(True):
		turn += 1
		if turn > numPlayers:
			turn %= numPlayers
		if not players[turn] == "GHOST":
			break
	#print (s)
	print ("It is player " + str(turn) + "'s turn:  " + s),
	while True:
		x = kbfunc()
		if not x == False:
			letter = x.decode()
			break
	if letter == ".":
		turn -= 1
		if turn == 0:
			turn = numPlayers
		currWord = s
		tempDict = wordsTree
		while len(currWord) > 0:
			single = currWord[:1]
			currWord = currWord[1:]
			if single in tempDict:
				tempDict = tempDict[single]
			else:
				tempDict = {}
		hintList = []
		for key in tempDict:
			hintList.append(key)
		print ("Possible next letters: ", hintList)
	elif letter in numbers: 
		print ("Player ", letter, " challenges Player ", prev)
		if s in wordsSet:
			fault = int(prev)
			turn = prev-1
		else:
			isWord = True
			currWord = s
			tempDict = wordsTree
			while len(currWord) > 0:
				single = currWord[:1]
				currWord = currWord[1:]
				if single in tempDict:
					tempDict = tempDict[single]
				else:
					isWord = False
					break
			if isWord == True:
				fault = int(letter)
				turn = int(letter)-1
			else:
				fault = int(prev)
				turn = prev-1

		if players[fault] == "":
			players[fault] = "G"
		elif players[fault] == "G":
			players[fault] = "GH"
		elif players[fault] == "GH":
			players[fault] = "GHO"
		elif players[fault] == "GHO":
			players[fault] = "GHOS"
		else:
			players[fault] = "GHOST"
		print (players)
		stillIn = 0
		winner = 0
		for key in players:
			if not players[key] == "GHOST":
				stillIn += 1
				winner = key
		if stillIn == 1:
			print ("Player ", winner, " wins!")
			break
		s = ""
	else:
		s = s + letter






'''def printGraph(dictionary, depth):
	if len(dictionary) == 0:
		return
	for key in dictionary:
		print (" " * depth, key)
		printGraph(dictionary[key], depth+1)
printGraph(wordsTree, 0)'''