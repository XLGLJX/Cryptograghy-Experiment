import base64
import string
from Crypto.Util.strxor import strxor_c,strxor
def cal_Hamming_distance(s1: bytes, s2: bytes):
    assert len(s1) == len(s2)
    sum = 0
    for x,y in zip(s1, s2):
        z = x ^ y
        sum += bin(z).count("1")
    return sum

def get_key_size(txt):
    dis = []
    for size in range(2,40):
        blocks = [txt[i*size: min((i+1)*size, len(txt))] for i in range(len(txt)//size)]
        # sum=cal_Hamming_distance(blocks[0],blocks[1])
        sum = 0
        for i in range(len(blocks)-2):
            sum += cal_Hamming_distance(blocks[i], blocks[i+1])
        dis.append((sum/(len(blocks)-2)/size, size))
    dis.sort()
    return dis[0][1]

def cal_Chi_squared_Statistic(msg):
    freqs = {
        'a': 0.0651738,
        'b': 0.0124248,
        'c': 0.0217339,
        'd': 0.0349835,
        'e': 0.1041442,
        'f': 0.0197881,
        'g': 0.0158610,
        'h': 0.0492888,
        'i': 0.0558094,
        'j': 0.0009033,
        'k': 0.0050529,
        'l': 0.0331490,
        'm': 0.0202124,
        'n': 0.0564513,
        'o': 0.0596302,
        'p': 0.0137645,
        'q': 0.0008606,
        'r': 0.0497563,
        's': 0.0515760,
        't': 0.0729357,
        'u': 0.0225134,
        'v': 0.0082903,
        'w': 0.0171272,
        'x': 0.0013692,
        'y': 0.0145984,
        'z': 0.0007836,
        ' ': 0.1918182
    }
    try:
        tmp = msg.decode()
    except:
        return 1e8
    f = lambda c: freqs[c] * len(tmp)
    return sum((tmp.count(c) - f(c))**2 / f(c) for c in string.ascii_lowercase)

def get_key_c(msg):
    l = []
    for i in range(256):
        tmp = strxor_c(msg, i)
        cnt = 0
        for c in tmp:
            if chr(c) in string.ascii_letters:
                cnt += 1
        l.append((cnt, i))
    return sorted(l)[-1][1]

def get_key_c_statisic(index,msg):
    l = []
    for i in range(256):
        tmp = strxor_c(msg, i)
        l.append((cal_Chi_squared_Statistic(tmp), i))
    return sorted(l)[0][1]

txt = open(r"D:\~~~homework\Crypto experiment\cryptopals\Set1\6.txt","rb").read()
txt = base64.b64decode(txt)

KEYSIZE = get_key_size(txt)
print(KEYSIZE)

blocks = [b"" for _ in range(KEYSIZE)]
for i in range(len(txt)):
    blocks[i%KEYSIZE]+=bytes([txt[i]])

key = b""
for index,block in enumerate(blocks):
    key += bytes([get_key_c_statisic(index, block)])
print(key)
c_key = key*(len(txt)//len(key))+key[:len(txt)%len(key)]
plain = strxor(txt,c_key).decode()
print(plain)
