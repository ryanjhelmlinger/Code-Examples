import sys

alphabetDict = {"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8, "i":9, "j":10, "k":11, "l":12, "m":13, "n":14, "o":15, "p":16, "q":17, "r":18, "s":19, "t":20, "u":21, "v":22, "w":23, "x":24, "y":25, "z":26}


def caeser_shift(message, char):
	shift = alphabetDict[char]-1
	cipher = ""
	for letter in message:
		newascii = ord(letter)+shift
		if newascii > 122:
			newascii = newascii - 26
		if newascii < 97:
			newascii = newascii + 26
		newchar = chr(newascii)
		cipher += newchar
	return cipher

def caeser_unshift(message, char):
	shift = -1*(alphabetDict[char]-1)
	cipher = ""
	for letter in message:
		newascii = ord(letter)+shift
		if newascii > 122:
			newascii = newascii - 26
		if newascii < 97:
			newascii = newascii + 26
		newchar = chr(newascii)
		cipher += newchar
	return cipher

def caeser_brute_force(message):
	for char in alphabetDict:
		text = caeser_shift(message, char)
		print(text)

def vignere_encode(message, keyword):
	keyLength = len(keyword)
	count = 0
	text = ""
	for letter in message:
		newLetter = caeser_shift(letter,keyword[count%keyLength])
		count+=1
		text += newLetter
	return text

def vignere_decode(message, keyword):
	keyLength = len(keyword)
	count = 0
	text = ""
	for letter in message:
		newLetter = caeser_unshift(letter,keyword[count%keyLength])
		count+=1
		text += newLetter
	return text

def get_frequencies(ciphertext):
	freqDict = {}
	for letter in ciphertext:
		if letter not in freqDict:
			freqDict[letter] = 1
		else: 
			freqDict[letter] += 1	 
	return freqDict


def index_of_coincidence(ciphertext):
	freqDict = get_frequencies(ciphertext)
	total = 0
	ciphertext.split()
	cipherLen = len(ciphertext)
	for key in freqDict:
		total += (freqDict[key]*(freqDict[key]-1)/(cipherLen*(cipherLen-1)))
	print(total)

def skip_text(ciphertext, keyword, offset)

plaintext = "thisisanexampletexthopefullyitworkssothaticanbefinishedwiththislab"
char = "b"

index_of_coincidence(plaintext)