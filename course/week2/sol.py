

import numpy
from Crypto.Util.strxor import strxor

cipher = "F96DE8C227A259C87EE1DA2AED57C93FE5DA36ED4EC87EF2C63AAE5B9A7EFFD673BE4ACF7BE8923CAB1ECE7AF2DA3DA44FCF7AE29235A24C963FF0DF3CA3599A70E5DA36BF1ECE77F8DC34BE129A6CF4D126BF5B9A7CFEDF3EB850D37CF0C63AA2509A76FF9227A55B9A6FE3D720A850D97AB1DD35ED5FCE6BF0D138A84CC931B1F121B44ECE70F6C032BD56C33FF9D320ED5CDF7AFF9226BE5BDE3FF7DD21ED56CF71F5C036A94D963FF8D473A351CE3FE5DA3CB84DDB71F5C17FED51DC3FE8D732BF4D963FF3C727ED4AC87EF5DB27A451D47EFD9230BF47CA6BFEC12ABE4ADF72E29224A84CDF3FF5D720A459D47AF59232A35A9A7AE7D33FB85FCE7AF5923AA31EDB3FF7D33ABF52C33FF0D673A551D93FFCD33DA35BC831B1F43CBF1EDF67F0DF23A15B963FE5DA36ED68D378F4DC36BF5B9A7AFFD121B44ECE76FEDC73BE5DD27AFCD773BA5FC93FE5DA3CB859D26BB1C63CED5CDF3FE2D730B84CDF3FF7DD21ED5ADF7CF0D636BE1EDB79E5D721ED57CE3FE6D320ED57D469F4DC27A85A963FF3C727ED49DF3FFFDD24ED55D470E69E73AC50DE3FE5DA3ABE1EDF67F4C030A44DDF3FF5D73EA250C96BE3D327A84D963FE5DA32B91ED36BB1D132A31ED87AB1D021A255DF71B1C436BF479A7AF0C13AA14794"
cipher = bytes.fromhex(cipher)
ans = ""

import string
import tqdm
def brute_spec_vig(Len):
    def get_group():
        tmp = []
        for i in range(Len):
            j = 0
            l = []
            while i+j*Len<len(cipher):
                l.append(cipher[i+j*Len])
                j+=1
            tmp.append(l)
        return tmp
    
    print(f"Begin to brute length key {Len}")
    sum = 0
    c_group = get_group()
    for l in c_group:
        for k in tqdm.trange(256):
            flag = True
            for b in l:
                a = chr(b^k)
                if a in string.ascii_letters or a in string.punctuation or a == ' ':
                    pass
                else:
                    flag = False
                    break
            if flag:
                sum += 1
        if sum != 0:
            print(sum)
        else:
            return False
    return True

def many_time_pad(Len):
    def know(index, pos, ch):
        if len(ch)!=1:
            s = b"".join([bytes([x]) for x in mt[index]])
            tmp = s.find(ch.encode())-1
            print("tmp: ",tmp)
            ch = pos
            pos = tmp
        mt[index, pos] = ord(ch)
        for x in range(len(c)):
            if x != index:
                mt[x][pos] = strxor(c[x], c[index])[pos] ^ ord(ch)

    def infer(index, pos):
        if mt[index, pos] != 0:
            return
        mt[index, pos] = ord(' ')
        for x in range(len(c)):
            if x != index:
                mt[x][pos] = strxor(c[x], c[index])[pos] ^ ord(' ')

    def cnt(pos, res):
        sum = 0
        for s in res:
            if chr(s[pos]).isalpha():
                sum += 1
        return sum

    def getSpace():
        for index, x in enumerate(c):
            res = [strxor(x, y) for y in c if x != y]
            for pos in range(len(x)):
                dat.append((cnt(pos, res), index, pos))

    dat = []

    MSGS = []
    for i in range(len(cipher)//Len):
        MSGS.append(cipher[i*Len:(i+1)*Len])

    
    min_len = min(len(x) for x in MSGS)
    print(min_len)
    
    c = [x[:min_len] for x in MSGS]
    
    mt = numpy.zeros([len(c), len(c[0])], dtype=int)

    print(len(mt[0]))
    getSpace()

    dat = sorted(dat)[::-1]

    for x in dat:
        infer(x[1], x[2])

    print()
    print("Possible plaintext:")
    global ans
    for index,s in enumerate(mt):
        print(index,": ",end='')
        for x in s:
            print(chr(x), end='')
            ans += chr(x)
        print()
    print()

    key = strxor(c[0], b''.join(bytes([x]) for x in mt[0]))   
    print("Maybe key: ",key)

if __name__ == '__main__':
    
    for Len in range(2,14):
        if brute_spec_vig(Len):
            many_time_pad(Len)
    print(cipher)
    print("ans: ", ans)