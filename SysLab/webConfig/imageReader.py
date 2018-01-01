#import Image
from PIL import Image
from PIL import ImageFilter
#from tesseract import image_to_string
import pytesseract
import io
from string import whitespace

import builtins

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

original_open = open
def bin_open(filename, mode='rb'):
	return original_open(filename, mode)
	
numberSet = set(['0','1','2','3','4','5','6','7','8','9'])

def seperateClues(imgText):
	global numberSet
	clues = []
	newLine = False
	clue = ''
	for char in imgText:
		if char in numberSet and newLine:
			clues.append(clue)
			clue = ''
		if char!="\n":
			clue+=char
			newLine = False
		else:
			clue+=" "
			newLine = True
	if clue!='\n' and len(clue)>0:
		clues.append(clue)
	return(clues)

def turnToDict(clues):
	global numberSet
	#acrossDict = {}
	#downDict = {}
	#across = True
	#prevNumber = 0
	clueDict = {}
	for clue in clues:
		number = ''
		for char in clue:
			if char in numberSet: number += char
			else: break
		if len(number)>0:
			if ' ' in clue:
				clueStart = clue.index(" ")
				actualClue = clue[clueStart+1:]
				if len(actualClue.translate(dict.fromkeys(map(ord, whitespace))))!=0:
					#print(int(number))
					#if int(number) < prevNumber:
					#	across = False
					#if across==True:
					#	prevNumber = int(number)
					#	acrossDict[int(number)] = actualClue
					#else:
					#	downDict[int(number)] = actualClue
					clueDict[int(number)] = actualClue
	#return (acrossDict,downDict)
	return clueDict


def readText(filename):
	img = Image.open(filename)

	width,height = img.size
	newWidth = 1250
	newHeight = int((height*width)/newWidth)
	size_tuple = (newWidth,newHeight)
	img = img.resize(size_tuple)

	#img = img.filter(ImageFilter.SHARPEN)

	try:
		builtins.open = bin_open
		bts = pytesseract.image_to_string(img)
	finally:
		builtins.open = original_open

	imgText = str(bts, 'UTF-8', 'ignore')

	print(imgText)

	#clues = seperateClues(imgText)

	acrossIndex = imgText.index("ACROSS")
	downIndex = imgText.index("DOWN")

	acrossClues = seperateClues(imgText[acrossIndex+6:downIndex])
	downClues = seperateClues(imgText[downIndex+4:])

	acrossCluesDict = turnToDict(acrossClues)
	downCluesDict = turnToDict(downClues)

	#(acrossCluesDict,downCluesDict) = turnToDict(clues)

	return (acrossCluesDict,downCluesDict)



	'''print("ACROSS\n")
	for clue in acrossCluesDict:
		print(clue, ": ", acrossCluesDict[clue])
	print("\n\nDOWN\n")
	for clue in downCluesDict:
		print(clue, ": ", downCluesDict[clue])'''



#readText('NYT_Crossword.jpeg')