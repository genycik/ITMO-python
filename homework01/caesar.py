def encrypt_caesar(plaintext: str, shift: int) -> str:
	"""
	Encrypts plaintext using a Caesar cipher.

	>>> encrypt_caesar("PYTHON")
	'SBWKRQ'
	>>> encrypt_caesar("python")
	'sbwkrq'
	>>> encrypt_caesar("Python3.6")
	'Sbwkrq3.6'
	>>> encrypt_caesar("")
	''
	"""
	cliphertext = ''
	for i in range(len(plaintext)):
		if ord('a') <= ord(plaintext[i]) <= ord('z'):
			g = ord(plaintext[i]) + shift
			if g > ord('z'):
				g -= 26
			cliphertext += chr(g)
		elif ord('A') <= ord(plaintext[i]) <= ord('Z'):
			g = ord(plaintext[i]) + shift
			if g > ord('Z'):
				g -= 26
			cliphertext += chr(g)
		else:
			cliphertext += plaintext[i]
	return cliphertext


def decrypt_caesar(ciphertext: str, shift: int) -> str:
	"""
	Decrypts a ciphertext using a Caesar cipher.

	>>> decrypt_caesar("SBWKRQ")
	'PYTHON'
	>>> decrypt_caesar("sbwkrq")
	'python'
	>>> decrypt_caesar("Sbwkrq3.6")
	'Python3.6'
	>>> decrypt_caesar("")
	''
	"""
	plaintext = ''
	for i in range(len(ciphertext)):
		if ord('a') <= ord(ciphertext[i]) <= ord('z'):
			g = ord(ciphertext[i]) - shift
			if g < ord('a'):
				g += 26
			plaintext += chr(g)
		elif ord('A') <= ord(ciphertext[i]) <= ord('Z'):
			g = ord(ciphertext[i]) - shift
			if g < ord('A'):
				g += 26
			plaintext += chr(g)
		else:
			plaintext += ciphertext[i]
	return plaintext

