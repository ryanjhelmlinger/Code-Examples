from sympy import *


def matrix_mod(M, m):
    return M.applyfunc(lambda x: Mod(x, m))


class Cryptoalphabet:
    def __init__(self, alphabet):
        #self.alphabet = alphabet.upper()
        self.alphabet = alphabet
        self.m = len(self.alphabet)

    def getIndex(self, c):
        #c = c.upper()
        return self.alphabet.index(c)

    def charNum(self, i):
        i = i % len(self.alphabet)
        return self.alphabet[i]

    def prepare(self, s):
        v = ""
        for c in s:
            if c in self.alphabet:
                #v = v + c.upper()
                v = v + c
        return v

    def digraphToInt(self, s):
        firstPosition = self.getIndex(s[0])
        secondPosition = self.getIndex(s[1])
        return firstPosition*26+secondPosition

    def intToDigraph(self, i):
        firstLetter = self.charNum(i//26)
        secondLetter = self.charNum(i%26)
        digraph = "" + firstLetter + secondLetter
        return (digraph)

    def pad_s(self, s, padchar="X"):
        """ Add padchar (default 'X') to s if length of s is odd"""
        if len(s)%2!=0:
            s += padchar
        return (s)
    
    def pad_a(self, a, padchar="X"):
        """ Add the numerical value of padchar (default 'X') to list a if length of a is odd """
        if len(a)%2!=0:
            numerical = self.getIndex(padchar)
            a.append(numerical)
        return (a)
    
    def StoM(self, S):
        """ Return a 2 x C matrix formed from the even-length string S, where C = len(S)/2"""
        assert len(self.stoa(S))%2==0
        return Matrix(self.stoa(S)).reshape(len(self.stoa(S)) // 2, 2).transpose()

    def MtoS(self, M):
        """ Turn a 2 x C matrix of numbers into a string S, where len(S) = C*2 """
        vertical = M.transpose()
        oneD = vertical.reshape(len(vertical), 1)
        arrayform = list(oneD)
        S = self.atos(arrayform)
        return (S)
    
    def stoa(self, s):
        """ Turn a string s into an (even-length) list of numbers, using getIndex(),
            padding the string with an extra char at the end if necessary """
        arrayform = []
        s = self.pad_s(s)
        for letter in s:
            arrayform.append(self.getIndex(letter))
        return (arrayform)
    
    def atos(self, a):
        """ Turn a list of numbers into a string, using charNum(),
            does not assume len(a) is even """
        S = ""
        a = self.pad_a(a)
        for number in a:
            S += self.charNum(number)
        return (S)