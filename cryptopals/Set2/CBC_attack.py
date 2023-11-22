
from Crypto.Util.strxor import strxor
from random import randbytes
from base64 import b64decode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

def _attack_block(padding_oracle, iv, c):
    r = bytes()
    for i in reversed(range(16)):
        s = bytes([16 - i] * (16 - i))
        for b in range(256):
            iv_ = bytes(i) + strxor(s, bytes([b]) + r)
            if padding_oracle(iv_, c):
                r = bytes([b]) + r
                break
        else:
            raise ValueError(f"Unable to find decryption for {s}, {iv}, and {c}")

    return strxor(iv, r)


def attack(padding_oracle, iv, c):
    p = _attack_block(padding_oracle, iv, c[0:16])
    for i in range(16, len(c), 16):
        p += _attack_block(padding_oracle, c[i - 16:i], c[i:i + 16])

    return p

def encrypt(key, p):
    iv = randbytes(16)
    cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
    c = cipher.encrypt(pad(p, AES.block_size))
    return iv, c

def decrypt(key, iv, c):
    cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
    p = cipher.decrypt(c)
    return p

def check_valid_padding(key, iv, c):
    try:
        unpad(decrypt(key, iv, c), 16)
        return True
    except ValueError:
        return False

plaintext = [
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]

key = randbytes(16)
for m in plaintext:
    p = b64decode(m)
    iv,c = encrypt(key, p)
    p_ = attack(lambda iv, c: check_valid_padding(key, iv, c), iv, c) 
    print(p)
    print(p_)
    print("="*10)