import sys
f = open("code2.txt", "r")
text = ""
for things in f: text += things
#print (text)
freqArray = {}
for char in text:
	if char in "QWERTYUIOPASDFGHJKLZXCVBNM.,":
		if char in freqArray: freqArray[char] += 1
		else: freqArray[char] = 1
finalVal = 0
for letter in freqArray: finalVal += (freqArray[letter]/len(text))*((freqArray[letter]-1)/(len(text)-1))
print(finalVal/.0385)