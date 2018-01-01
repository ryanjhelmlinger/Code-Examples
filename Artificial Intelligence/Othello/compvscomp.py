
def compChoose2(board, turnLetter):
	possibleMoves = findPossibilities(board, turnLetter)
	index, num = random.choice(list(possibleMoves))
	board = inputSpot(board, index, turnLetter)
	if turnLetter == "O": turnLetter = "X"
	else: turnLetter = "O"
	return [board, turnLetter]


def possPass(board, tl):
	oposs, xposs = findPossibilities(board, "O"), findPossibilities(board, "X")
	if len(xposs)==0:
		if len(oposs)==0: return "*"
		else: tl = "O"
	if len(oposs)==0: tl = "X"
	return tl


first = sys.argv[1].lower()
second = sys.argv[2].lower()
third = 0
if len(sys.argv)>3:
	third = sys.argv[3]


if first=="c" and second=="c" and third==0:
	while True:
		showBoard(board)
		turnLetter = possPass(board, turnLetter)
		if turnLetter == "*": break
		if turnLetter == "X": board, turnLetter = compChoose3(board, turnLetter)
		else: board, turnLetter = compChoose2(board, turnLetter)
		print("It is player " + turnLetter + "'s turn:  ")
else:
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