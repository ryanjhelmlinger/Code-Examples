import sys

if len(sys.argv)<3:
	print("no work")
else:
	keyword, message = sys.argv[1], sys.argv[2]
	print("Keyword: " + keyword + "\nmessage: " + message)
	usedArray, newKeyword = [], ""
	for letter in keyword:
		if letter not in usedArray and not letter==" ":
			usedArray.append(letter)
			newKeyword += letter
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	encodeMatrix = newKeyword
	for letter in alphabet:
		if letter not in encodeMatrix: 
			encodeMatrix += letter
	encoder = ""
	for i in range(0,5):
		for j in range (0,4): 
			encoder += encodeMatrix[j*7+i]
	for i in range (5, 7):
		for j in range (0,3): 
			encoder += encodeMatrix[j*7+i]
	cipher = ""
	for letter in message:
		count = 0
		for part in encoder:
			if part==letter: break
			else: count+=1
		cipher += alphabet[count]
	print("\n"+cipher)