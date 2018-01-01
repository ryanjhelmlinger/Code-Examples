from MatrixCiphers import *
from Cryptoalphabet import *

print("-"*50)
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