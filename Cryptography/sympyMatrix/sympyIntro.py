from sympy import *

from sympy.solvers.solveset import linsolve


def printOut(A):
	length = A.shape[1]
	for i in range(0,length):
		for j in range(0,2):
			for letter in alphaDict:
				if alphaDict[letter]==int(A[j,i]): print(letter, end=" ")

def matrix_mod(A,m):
	return A.applyfunc(lambda x: Mod(x,m))

alphaDict = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9,"K":10,"L":11,"M":12,"N":13,"O":14,"P":15,"Q":16,"R":17,"S":18,"T":19,"U":20,"V":21,"W":22,"X":23,"Y":24,"Z":25, ",":26, ".":27, "'":28, "?":29, "/":30}

Decoded = Matrix([[23,8],[24,9]])
Encoded = Matrix([[19,4],[7,17]])
EncMess = Matrix([[0,20,24,20,4,15,12,20,16],[10,22,14,25,21,14,0,24,10]])

print(Decoded.inv_mod(26))

aInv = Encoded*(Decoded.inv_mod(26))
print(matrix_mod(aInv,26))
message = aInv*EncMess
solution = matrix_mod(message,26)

printOut(solution)