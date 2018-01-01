from sympy import *
from random import *

def choose_modulus(k, l, d):
	#returns (P1, P2) where 2^k < Pi < 2^l and log_2(P1) + d < log_2(P2)
	#(the idea is that 2^k and 2^ are bounds on the two primes, but the two primes are also)
	#(at least 2^d apart. The modulus is = P1*P2, but you return the primes)
	P1 = 0
	P2 = 0
	while (abs(P2-P1)<2**d):
		P1 = randprime(2**k, 2**l)
		P2 = randprime(2**k, 2**l)
	return (P1, P2)

def choose_encryption_key(p1, p2):
	#let m = p1 * p2
	#returns a number 1<e<m such that gcd(e, phi(m)) = 1
	choices = []
	mygcd = -1
	m = p1 * p2
	phi = (p1-1)*(p2-1)
	for i in range(int(m/7),m):
		mygcd = gcd(i,phi)[0]
		if mygcd==1:
			return i
	return -1

def compute_decryption_key(e, p1, p2):
	#returns the decryption key d = e-inverse mod phi(p1*p2)
	phi = (p1-1)*(p2-1)
	return inv_mod(e,phi)

def RSA_encrypt(P, e, m):
	#if P is an integer, returns the encrypted integer C from RSA encryption
	return power_mod(P,e,m)

def RSA_decrypt(C, d, m):
	#if C is an integer, returns the decrypted integer C
	return power_mod(C,d,m)

def RSA_crack(C, e, m):
	#If C is an integer, compute the decryption key d from e and m and
	#return the plaintext P you can use built-in totient() or any other sympy methods
	d = inv_mod(e,totient(m))
	#d = (e**-1) % totient(m)
	P = RSA_decrypt(C,d,m)
	return (P)

def power_mod(a, b, m):
	#computes a**b mod m when a**b is very large
	return pow(a,b,m)

def string_to_int(s):
	# returns an integer from the ASCII encoding of s
	return int.from_bytes(s.encode(),'big')

def int_to_string(n):
	# returns a string from the integer n
	return n.to_bytes((n.bit_length()+7)//8,'big').decode()

def gcd(b, n):
    #Return g, x0, y0 such that x0*b + y0*n = g and g is the gcd of (b,n)
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0


def inv_mod(b, n):
    #Return the modular inverse of b mod #or None if gcd(b,n) > 1
    g, x, _ = gcd(b, n)
    if g == 1:
        return x % n