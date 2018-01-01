from Cryptoalphabet import *
from sympy import *
from random import randint

def encrypt(E, p, a):
    """Apply matrix E to string p mod 26 and return an encrypted string,
       relative to Cryptoalphabet a """
    return a.MtoS(matrix_mod(E*a.StoM(p),len(a.alphabet)))

def decrypt(D, c, a):
    """Apply matrix D to string c mod 26 and return a decrypted string,
       relative to Cryptoalphabet a """
    pass

def get_decryption_matrix(P,C, a):
    """ Knowing two digraphs in string P are encoded as string C, determine
        a unique decryption matrix, relative to Cryptoalphabet a """
    pass

def get_random_invertible_matrix(m):
    """ return a random 2x2 matrix M with gcd(det(M),m)= 1 """
    d = 2
    while d>1:
        # make a random 2x2 matrix, M, and let d = gcd(M, m)
    return M
