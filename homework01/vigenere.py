import string


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
        >>> encrypt_vigenere("PYTHON", "A")
        'PYTHON'
        >>> encrypt_vigenere("python", "a")
        'python'
        >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
        'LXFOPVEFRNHR'
        """
    ciphertext = ""
    keyword *= (len(plaintext)//len(keyword)) + 1
    for j in range(len(plaintext)):
            up = False
            if plaintext[j].isupper():
                up = True
            if plaintext[j].lower() in string.ascii_lowercase:
                a = string.ascii_lowercase.index(keyword[j].lower())
                b = string.ascii_lowercase.index(plaintext[j].lower())
                c = (a + b) % len(string.ascii_lowercase)
                if up:
                    ciphertext += string.ascii_lowercase[c].upper()
                else:
                    ciphertext += string.ascii_lowercase[c]
            else:
                plaintext += ciphertext[j]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
        >>> decrypt_vigenere("PYTHON", "A")
        'PYTHON'
        >>> decrypt_vigenere("python", "a")
        'python'
        >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
        'ATTACKATDAWN'
        """
    plaintext = ""
    keyword *= (len(ciphertext) // len(keyword)) + 1
    for j in range(len(ciphertext)):
            up = False
            if ciphertext[j].isupper():
                up = True
            if ciphertext[j].lower() in string.ascii_lowercase:
                a = string.ascii_lowercase.index(ciphertext[j].lower())
                b = string.ascii_lowercase.index(keyword[j].lower())
                c = (a - b) % len(string.ascii_lowercase)
                if up:
                    plaintext += string.ascii_lowercase[c].upper()
                else:
                    plaintext += string.ascii_lowercase[c]
            else:
                plaintext += ciphertext[j]
    return plaintext