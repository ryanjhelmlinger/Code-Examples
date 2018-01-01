from sympy import *


def matrix_mod(M, m):
    return M.applyfunc(lambda x: Mod(x, m))


class Cryptoalphabet:
    def __init__(self, alphabet):
        self.alphabet = alphabet.upper()
        self.m = len(self.alphabet)

    def getIndex(self, c):
        c = c.upper()
        return self.alphabet.index(c)

    def charNum(self, i):
        i = i % len(self.alphabet)
        return self.alphabet[i]

    def prepare(self, s):
        v = ""
        for c in s:
            if c in self.alphabet:
                v = v + c.upper()
        return v

    def digraphToInt(self, s):
        # return an int computed from the indices of s
        pass

    def intToDigraph(self, i):
        # return a digraph computed from the integer i
        pass

    def pad_s(self, s, padchar="X"):
        """ Add padchar (default 'X') to s if length of s is odd"""
        if len(s)%2!=0:
            s+=padchar
        return s
    
    def pad_a(self, a, padchar="X"):
        if len(a)%2!=0:
            a.append(self.alphabet.getIndex(padchar))
        return a
        """ Add the numerical value of padchar (default 'X') to list a if length of a is odd """
        # you may not need this function in your code
    
    def StoM(self, S):
        """ Return a 2 x C matrix formed from the even-length string S, where C = len(S)/2"""
        assert len(self.stoa(S))%2==0
        return Matrix(self.stoa(S)).reshape(len(self.stoa(S)) // 2, 2).transpose()

    def MtoS(self, M):
        s = ""
        length = M.shape[1]
        for i in range(0,length):
            for j in range(0,2): s+=self.alphabet[M[j,i]]
        return s
        """ Turn a 2 x C matrix of numbers into a string S, where len(S) = C*2 """
        pass
    
    def stoa(self, s):
        """ Turn a string s into an (even-length) list of numbers, using getIndex(),
            padding the string with an extra char at the end if necessary """
        pass
    
    def atos(self, a):
        """ Turn a list of numbers into a string, using charNum(),
            does not assume len(a) is even """
    pass
