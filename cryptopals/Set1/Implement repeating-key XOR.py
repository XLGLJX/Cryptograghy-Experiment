import itertools
from Crypto.Util.strxor import strxor
key = b'ICE'
plain = b"""Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

c_key = key*(len(plain)//len(key))+key[:len(plain)%len(key)]
print(strxor(plain,c_key).hex())