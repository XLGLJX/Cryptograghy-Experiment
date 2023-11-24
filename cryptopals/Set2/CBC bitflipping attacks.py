import random
from Crypto.Util.number import getRandomInteger, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor
import base64
from functions import cbc_encrypt, cbc_decrypt

key = bytes([random.randint(0,2**8-1) for _ in range(16)])
iv = bytes([random.randint(0,2**8-1) for _ in range(16)])
predata = b"comment1=cooking%20MCs;userdata="
suffixdata = b";comment2=%20like%20a%20pound%20of%20bacon"
goal_msg = b";admin=true;"  
def account_encrypt(data=b""):
    if goal_msg in data:
        raise ValueError
    plaintxt = pad(predata + data + suffixdata, AES.block_size)
    return cbc_encrypt(plaintxt, key, iv)

def check_admin(cipher: bytes):
    plain = cbc_decrypt(cipher, key, iv)
    print(f"plain: {plain}")
    return goal_msg in plain

if __name__ == "__main__":
    pre_len = len(predata)              # 32
    print(pre_len)
    suf_len = len(suffixdata)
             # 12
    blocksize = AES.block_size
    attack_msg = b";admin=truE;".ljust(blocksize, b' ')
    cipher = account_encrypt(attack_msg)
    tmp = cipher[blocksize:2*blocksize]
    after_enc = strxor(tmp, attack_msg) 
    replace_cipher = strxor(after_enc, goal_msg.ljust(blocksize, b' '))

    print(f"{goal_msg} in plain is: {check_admin(cipher[:blocksize]+replace_cipher+cipher[2*blocksize:])}")