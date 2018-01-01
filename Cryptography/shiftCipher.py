import sys

if len(sys.argv)==1:
	print("no message")
else:
	message = sys.argv[1]
	print(message)
	shift = 1
	cipher = ""
	for letter in message:
		newascii = ord(letter)+shift
		if newascii > 122:
			newascii = newascii - 26
		if newascii < 97:
			newascii = newascii + 26
		newchar = chr(newascii)
		cipher += newchar
	print(cipher)