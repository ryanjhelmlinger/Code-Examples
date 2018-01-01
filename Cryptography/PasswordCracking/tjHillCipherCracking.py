from MatrixCiphers import *
from Cryptoalphabet import *
from sympy import *

user,password,count,userPasswords="","",0,{}
with open("userPasswords.txt") as f:
	for line in f:
		for word in line.split():
			if count%2==0:
				user = word
			else:
				password = word
			count+=1
		userPasswords[user] = password

commonPasswords=[]
with open("commonPasswords.txt") as f:
	for line in f:
		for word in line.split():
			if len(word)>6: commonPasswords.append(word.upper())

#print(len(commonPasswords))
#print(len(userPasswords))
code1 = ""
for i in range(33,94):
	code1+=chr(i)
code1 = Cryptoalphabet(code1)

count = 0
for user in userPasswords:
	count+=1
	#if count%10==0:
		#print(count)
	encryptedPassword = userPasswords[user]
	for commPassword in commonPasswords:
		if len(commPassword)>len(encryptedPassword): continue
		midStep = get_decryption_matrix(commPassword[0:4],encryptedPassword[0:4],code1)
		if midStep==False: 
			#print("here")
			continue
		realPassword = decrypt(midStep,encryptedPassword,code1)
		#print(realPassword[0:len(commPassword)], commPassword)
		if realPassword[0:len(commPassword)] == commPassword:
			print(user, ": ", decrypt(midStep,encryptedPassword,code1))
			print()
			for testUser in userPasswords:
				print(testUser, ": ", decrypt(midStep,userPasswords[testUser],code1))
			print()
			print()
			continue
