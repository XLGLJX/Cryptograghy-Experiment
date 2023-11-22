import string
from Crypto.Util.strxor import strxor_c

txt = open(r"D:\~~~homework\Crypto experiment\cryptopals\Set1\4.txt",'r').readlines()
txt = [s.strip() for s in txt]
for i in range(256):
    for s in txt:
        tmp = strxor_c(bytes.fromhex(s), i)
        cnt = 0
        for c in tmp:
            if chr(c) in string.printable:
                cnt += 1
        if cnt == len(s)>>1:
            print(tmp)
            