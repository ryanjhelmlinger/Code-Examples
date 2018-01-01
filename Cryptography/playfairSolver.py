import sys

keyword = "YELLOW"
decoded = "BODNBIVBMKUGGQGOEXPDCYBKYBCKQFVULOLXLOVBOT"
usedArray, newKeyword = [], ""
for letter in keyword:
	if letter not in usedArray:
		usedArray.append(letter)
		newKeyword += letter
alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
matrix = newKeyword
for letter in alphabet:
	if letter not in matrix:
		matrix += letter

finalMessage = ""
for i in range(0, int(len(decoded)/2)):
	first = decoded[2*i]
	second = decoded[2*i+1]
	firstIndex = secondIndex = 0
	count = 0
	for j in range(0, 25):
		if matrix[j] == first:
			firstIndex = count
		if matrix[j] == second:
			secondIndex = count
		count += 1
	fixed = False
	if firstIndex%5==secondIndex%5 and firstIndex%5!=0 and fixed==False:
		finalMessage += (matrix[firstIndex-1]+matrix[secondIndex-1])
		fixed=True
	if firstIndex%5==secondIndex%5 and firstIndex%5==0 and fixed==False:
		finalMessage += (matrix[firstIndex+4]+matrix[secondIndex+4])
		fixed=True
	sameVert = False
	for k in range(0,5):
		if firstIndex>=k*5 and firstIndex<(k+1)*5 and secondIndex>=k*5 and secondIndex<(k+1)*5:
			sameVert = True
	if sameVert==True and firstIndex<5 and fixed==False:
		finalMessage += (matrix[firstIndex+20]+matrix[secondIndex-5])
		fixed=True
	if sameVert==True and secondIndex<5 and fixed==False:
		finalMessage += (matrix[firstIndex-5]+matrix[secondIndex+20])
		fixed=True
	if sameVert==True and fixed==False:
		finalMessage += (matrix[firstIndex-5]+matrix[secondIndex-5])
		fixed=True

	if fixed == False:
		newFirstIndex = firstIndex + (secondIndex%5-firstIndex%5)
		newSecondIndex = secondIndex + (firstIndex%5-secondIndex%5)
		finalMessage += (matrix[newFirstIndex]+matrix[newSecondIndex])
print(finalMessage)
