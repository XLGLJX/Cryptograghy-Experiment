from Crypto.Cipher import AES
import base64
import binascii
from hashlib import sha1
 
iv = b"\x00"*AES.block_size
passport = '12345678<8<<<1110182<111116?<<<<<<<<<<<<<<<4'

def get_date_check_digit(date: str):
    return (int(date[0])*7+int(date[1])*3+int(date[2])+int(date[3])*7+int(date[4])*3+int(date[5]))%10

index = passport.find("?")
print("?=", get_date_check_digit(passport[index-6:index]))
# ?=7

passport = '12345678<8<<<1110182<1111167<<<<<<<<<<<<<<<4'
no = passport[:10]
birth = passport[13:20]
arrive = passport[21:28]
mrz = no + birth + arrive
MRZ = sha1(mrz.encode()).hexdigest()
print(MRZ)
# a095f0fdfe51e6ab3bf5c777302c473e7a59be65

def func(ka):
    k=[]
    a=bin(int(ka,16))[2:]
    for i in range(0,len(a),8):
        if(a[i:i+7].count('1')%2==0):
           k.append(a[i:i+7]+'1')
        else:
           k.append(a[i:i+7]+'0')
    knew=hex(int(''.join(k),2))
    return knew[2:]

k_seed = MRZ[:32]
c = '00000001'
d = k_seed + c
h_d = sha1(bytes.fromhex(d)).hexdigest()
# print(h_d) 5a998952aa381c5307909962536

ka = func(h_d[:16])
kb = func(h_d[16:32])
key = ka + kb
cipher = '9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI'
cipher = base64.b64decode(cipher)

aes = AES.new(bytes.fromhex(key), AES.MODE_CBC, iv)
result = aes.decrypt(cipher)
print(result)