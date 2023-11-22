import string
from Crypto.Util.strxor import strxor_c

s = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
for i in range(256):
    tmp = strxor_c(s,i)
    cnt = 0
    for c in tmp:
        if chr(c) in string.printable:
            cnt += 1
    if cnt == len(s):
        print(tmp)