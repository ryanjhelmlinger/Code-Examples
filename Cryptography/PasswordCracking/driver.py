from MatrixCiphers import *
from Cryptoalphabet import *
from sympy import *

"""code1 = Cryptoalphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ!' ")
matrixthing = Matrix([[1,4,6,2,3],[7,2,4,5,2]])
print (Cryptoalphabet.MtoS(code1, matrixthing))"""
 

print("-"*50)
print ("PART ONE")
print("Testing Hill Codes")
code1 = Cryptoalphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ!' ")
plaintext = "Don't Mine at Night!"
E = Matrix([[4,19],[13,10]])
ciphertext = encrypt(E, plaintext, code1)
print("'%s' encodes as '%s'" % (plaintext, ciphertext))
print("  using encryption matrix")
pprint(E)
print("And %s decrypts to %s" % (ciphertext, decrypt(E.inv_mod(code1.m),
                                                     ciphertext, code1)))

print("-"*50)
print("Cracking a code using crib text")
ciphertext = "!NITFOITTFW!ITFULBAY"
answer = decrypt(get_decryption_matrix("ESAT", "EIZS", code1),
                 ciphertext, code1)
print("ciphertext %s is %s" % (ciphertext, answer))

print("-"*50)
print ("PART TWO")
mycode = Cryptoalphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890. ")
plaintext = "I hope that this 1 message will be encoded correctly."
print ("Plaintext: " + plaintext)
E = get_random_invertible_matrix(mycode.m)
print ("Encryption Matrix:")
pprint (E)
ciphertext = encrypt(E, plaintext, mycode)
print ("Encryption: " + ciphertext)
decrypted = decrypt(E.inv_mod(mycode.m),ciphertext, mycode)
print ("Decrytion: " + decrypted)
print("-"*50)



code1 = Cryptoalphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ!.?")

print("-"*50)
readable = "TOER" #correct one
encrypted = "TMRI" #incorrect one
ciphertext = "FMXUDOCURFGMGVOLNUPORIFGLHTBBP.WTADHTVCMEU.G.WEHQ!ZAO.!JW!GOA?.W.G?BFTJJEUZACZXCEHPOHQ.WQG?YZ.DI.WSFRIV?WOIOUCXCQG.GRISJFU"

midStep = get_decryption_matrix(readable[0:4],encrypted[0:4],code1)
print(midStep)
realPassword = decrypt(midStep,ciphertext,code1)
print(realPassword)


print("-"*50)
print("-"*50)


print (len("ABCDEFGHIJKLMNOPQRSTUVWXYZ!.?0123456789-*"))

code1 = Cryptoalphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ!.?0123456789-*")

print("-"*50)
readable = "TOER" #correct one
encrypted = "AQ8J" #incorrect one
ciphertext = "M4468NZ.F0SR6*BD4GTOPKBV*1D7?TYSK"

midStep = get_decryption_matrix(readable[0:4],encrypted[0:4],code1)
print(midStep)
realPassword = decrypt(midStep,ciphertext,code1)
print(realPassword)


print("-"*50)
print("-"*50)


code1 = Cryptoalphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ!.?0123456789-*")

print("-"*50)
#readable = "TOER" #correct one
#encrypted = "AQ8J" #incorrect one
ciphertext = ""

#midStep = get_decryption_matrix(readable[0:4],encrypted[0:4],code1)
midStep2 = Matrix([[7,24],[4,3]])
print(midStep2)
midStep2 = matrix_mod(midStep2, 41)
print(midStep2)
midStep2 = Matrix([[18,20],[17,1]])
print(midStep2)
realPassword = decrypt(midStep2,ciphertext,code1)
print(realPassword)


print(mod_inverse(13,41))

print("-"*50)
print("-"*50)

midStep2 = Matrix([[7,24],[4,3]])
for i in range(0,41):
	for j in range(0,41):
		twoLetters = Matrix([[i],[j]])
		new = matrix_mod(midStep2*twoLetters,41)
		if(new==twoLetters):
			print(new)

print()
print()
print()
print("-"*50)
print("-"*50)
print("-"*50)
print("-"*50)
print("-"*50)
print("-"*50)
print("-"*50)
print("-"*50)
print()
print()
print()
print()
print()
print()

code1 = Cryptoalphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.! ")
code2 = Cryptoalphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ!.?0123456789 -*abcdefghijklmnopqrstuvwxyz")
print(len("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.! "))
print(len("ABCDEFGHIJKLMNOPQRSTUVWXYZ!.?0123456789 -*abcdefghijklmnopqrstuvwxyz"))
plaintext = "Only another week until Winter Break!".upper()
E = get_random_invertible_matrix(code2.m)
print ("Encryption Matrix:")
pprint (E)
ciphertext = encrypt(E, plaintext, code2)
print ("Encryption: " + ciphertext)
Einv = E.inv_mod(code2.m)
#Einv = matrix_mod(Einv,code1.m)
pprint(Einv)
decrypted = decrypt(Einv,ciphertext, code1)
print ("Decrytion: " + decrypted)
print ("Decrytion: " + plaintext)




'''
print("-"*50)
print ("PART TWO")
mycode = Cryptoalphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890. ")
plaintext = "I hope that this 1 message will be encoded correctly."
print ("Plaintext: " + plaintext)
E = get_random_invertible_matrix(mycode.m)
print ("Encryption Matrix:")
pprint (E)
ciphertext = encrypt(E, plaintext, mycode)
print ("Encryption: " + ciphertext)
decrypted = decrypt(E.inv_mod(mycode.m),ciphertext, mycode)
print ("Decrytion: " + decrypted)
print("-"*50)
'''