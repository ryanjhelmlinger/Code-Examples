from MatrixCiphers import *
from Cryptoalphabet import *
from sympy import *


#alphaDict = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9,"K":10,"L":11,"M":12,"N":13,"O":14,"P":15,"Q":16,"R":17,"S":18,"T":19,"U":20,"V":21,"W":22,"X":23,"Y":24,"Z":25, ",":26, ".":27, "'":28, "?":29, "/":30}
alphaDict = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9,"K":10,"L":11,"M":12,"N":13,"O":14,"P":15,"Q":16,"R":17,"S":18,"T":19,"U":20,"V":21,"W":22,"X":23,"Y":24,"Z":25}

def mod_inverse(a,m):
	for i in range(m):
		if a*i%m==1: return i
	return "none"

def lin_solve(a,b,c,m):
	inverse = mod_inverse(a,m)
	if inverse=="none": return "none"
	return inverse*(c-b)

def lin_sys_solve(a,b,c,d,e,f,m):
	x = lin_solve(a-d,0,c-f,m)
	if x=="none": return ("none","none")
	return (x,(c%m)-a*x)

def affineSolve(message,crib):
	(a,b) = lin_sys_solve(alphaDict[message[0]],1,alphaDict[crib[0]],alphaDict[message[1]],1,alphaDict[crib[1]],26)
	if a=="none": (a,b) = lin_sys_solve(alphaDict[message[1]],1,alphaDict[crib[1]],alphaDict[message[2]],1,alphaDict[crib[2]],26)
	if a=="none": (a,b) = lin_sys_solve(alphaDict[message[0]],1,alphaDict[crib[0]],alphaDict[message[2]],1,alphaDict[crib[2]],26)
	print(a,b)
	newMessage = ""
	for letter in message:
		for key in alphaDict:
			if alphaDict[key] == (alphaDict[letter]*a+b)%26: newMessage += key
	print(newMessage)


#message = ("RtalinawruncwgrupRirsfiwnajbswalrtafietrcmokirtswunnawrufa").upper()
#crib = ("The").upper()
#affineSolve(message, crib)

print(mod_inverse(13,41))
print(mod_inverse(475,676))
print(208953%676)

message = ("XMRPQ").upper()
a=3
b=-9

s = ""
for letter in message:
	#encrypt
	#newIndex = (a*alphaDict[letter]+b)%len(alphaDict)
	#decrypt
	newIndex = ((alphaDict[letter]-b)*mod_inverse(a,len(alphaDict)))%len(alphaDict)
	for key in alphaDict:
		if alphaDict[key]==newIndex:
			s += key
print(s)



allLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpha = Cryptoalphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
def affine_encode_digraphs(plaintext, a, b):
	plaintext = plaintext.upper()
	withoutPunc = ""
	for letter in plaintext:
		if letter in allLetters:
			withoutPunc += letter
	plaintext = withoutPunc
	if len(plaintext)%2==1:
		plaintext+="X"
	ciphertext = ""
	for i in range(int(len(plaintext)/2)):
		digraph = plaintext[i*2:i*2+2]
		x = alpha.digraphToInt(digraph)
		y = a*x+b
		y = y%(len(allLetters)**2)

		newdigraph = alpha.intToDigraph(y)
		ciphertext += newdigraph
	return ciphertext

print(affine_encode_digraphs("SSPXYOPX", 203, 203*-31))



print("-"*50)
print("-"*50)


alphaDict = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9,"K":10,"L":11,"M":12,"N":13,"O":14,"P":15,"Q":16,"R":17,"S":18,"T":19,"U":20,"V":21,"W":22,"X":23,"Y":24,"Z":25, "!":26, ".":27, "?":28, "0":29, "1":30, "2":31, "3":32, "4":33, "5":34, "6":35, "7":36, "8":37, "9":38, "-":39, "*":40}


a=14
b=0

message = ("K7EP?G0MJLYO?!D0GW6KMUBQ*-.FJ-").upper()
s = ""
for letter in message:
	#encrypt
	newIndex = (a*alphaDict[letter]+b)%len(alphaDict)
	#decrypt
	#newIndex = ((alphaDict[letter]-b)*mod_inverse(a,len(alphaDict)))%len(alphaDict)
	for key in alphaDict:
		if alphaDict[key]==newIndex:
			s += key
print(s)