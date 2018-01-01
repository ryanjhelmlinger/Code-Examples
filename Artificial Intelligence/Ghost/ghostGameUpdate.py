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

def getProb(wordSet, dictionary, word, turns):
	good, bad = 0, 0
	for key in dictionary:
		if word+key in wordSet:
			if turns%numPlayers == 1:
				good += 1
			else:
				bad += 1
		else:
			newList = getProb(wordSet, dictionary[key], word+key, turns+1)
			good += newList[0]
			bad += newList[1]
	return [good, bad]


def hint(prefix):
	currWord = prefix
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
	return hintList


def analyze(prefix, playerNum):
	if prefix in wordsSet and len(prefix)>3:
		return ({" "}, set())
	good, bad = set(), set()
	currWord = prefix
	tempDict = wordsTree
	while len(currWord) > 0:
		single = currWord[:1]
		currWord = currWord[1:]
		if single in tempDict:
			tempDict = tempDict[single]
		else:
			tempDict = {}
	for key in tempDict:
		tryGood, tryBad = analyze(prefix+key, (playerNum+1)%numPlayers)
		if len(tryGood) != 0:
			bad.add(key)
		else:
			good.add(key)
	return (good, bad)


		
wordsTree = {}
f = open("ghost.txt", "r")
wordsList = []
wordsSet = set([])
for line in f:
	wordsSet.add(line.split()[0])
	wordsList.append(line.split()[0])
for word in wordsList:
	makeTree(word, wordsTree)

computers = set([])
numPlayers = 0
for num in range(1, len(sys.argv)):
	if sys.argv[num] == "C":
		numPlayers += 1
		computers.add(numPlayers)
	else:
		numPlayers += int(sys.argv[num])
players = {}
for i in range(1, numPlayers+1):
	players[i] = ""


#print("Test: ", wordsTree['a']['a'])


#print(analyze("b", 10))
#print("\n")


numbers = set(["1", "2", "3", "4", "5", "6", "7", "8", "9", 1, 2, 3, 4, 5, 6, 7, 8, 9])
s = ""
challenger = -1
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
	#print (challenger)
	if turn not in computers or challenger != -1:
		#print ("It is player " + str(turn) + "'s turn: " + s),
		if challenger == -1:
			#print(s)
			print ("Player ", str(turn), ": ", s)
			while True:
				x = kbfunc()
				if not x == False:
					letter = x.decode()
					break
		else:
			letter = challenger
			challenger = -1
		#print (letter)
		if letter == ".":
			turn -= 1
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
			if letter in computers:
				print ("Player ", letter, " (computer) challenges Player ", prev)
			else:
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
			#print(s)
	else:
		print ("Player ", str(turn), ": ", s, flush=True),
		currWord = s
		tempDict = wordsTree
		possDict = {}
		while len(currWord) > 0:
			single = currWord[:1]
			currWord = currWord[1:]
			if single in tempDict:
				tempDict = tempDict[single]
			else:
				tempDict = {}
				compGuess = "~"
		if len(tempDict) == 0 or s in wordsSet and len(s)>3:
			#print ("comp wants to challenge")
			challenger = turn
			turn = prev

		else:
			bestProb = 0
			best = ""
			backup = ""
			possWin, nah = analyze(s, 10)
			if len(possWin) != 0:
				possibles = possWin
			else:
				possibles = nah
			for key in possibles:
				backup = key
				if s+key not in wordsSet or len(s+key)<4:
					gobList = getProb(wordsSet, tempDict[key], s+key, 1)
					#print (gobList)
					total = gobList[1]+gobList[0]
					if total != 0:
						prob = gobList[0]/total
						#print (key, ": ", prob)
						if prob>bestProb:
							bestProb = prob
							best = key
			if best == "":
				s = s + backup
			else:
				s = s + best
			#print ("Player ", turn, " (computer) added letter ", compGuess, " to the word:\t", s)
			#print ("Player ", str(turn), ": ", s, flush=True),




'''def printGraph(dictionary, depth):
	if len(dictionary) == 0:
		return
	for key in dictionary:
		print (" " * depth, key)
		printGraph(dictionary[key], depth+1)
printGraph(wordsTree, 0)'''