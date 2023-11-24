from functions import ecb_encrypt, ecb_decrypt,encryption_oracle
import random
from Crypto.Util.number import getRandomInteger, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor
import base64
import string

key = bytes([random.randint(0,2**8-1) for _ in range(16)])
prefix = bytes([random.randint(0,2**8-1) for _ in range(random.randint(0,32))])


def get_blocksize(cipher):
    for i in range(len(cipher)//2):
        for blocksize in range(8, (len(cipher)-i)//2):
            if cipher[i:i+blocksize] == cipher[i+blocksize: i+2*blocksize]:
                print(f"Block length: {blocksize}, i: {i}")
                return blocksize, i
    return (None, None)

if __name__ == "__main__":
    plain = """Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK"""
    plain = base64.b64decode(plain)
    my_string, cnt = "A", 1
    base_cipher = encryption_oracle(prefix+plain, key, False)[0]
    
    print(f"length prefix: {len(prefix)}")
    print(f"prefix: {prefix}")
    
    while True:
        cnt += 1
        my_string += "A"
        encrypted, answer = encryption_oracle(prefix+my_string.encode()+plain, key, False)
        blocksize, prefix_len = get_blocksize(encrypted)
        if blocksize:
            prefix_len -= cnt % blocksize
            break
    print(f"cal length of prefix: {prefix_len}")
    
    pre_block_size = prefix_len//blocksize if prefix_len%blocksize==0 else prefix_len//blocksize+1
    print(f"pre_block_size: {pre_block_size}")
    cnt = pre_block_size*blocksize
    ans = b"A"*(pre_block_size*blocksize + blocksize-1)
    while True: 
        if len(ans)-blocksize+1 >= len(base_cipher) + blocksize*pre_block_size-len(prefix):
            break
        my_prefix = ans[cnt: cnt+blocksize-1]
        index = cnt//blocksize
        encrypted, _ = encryption_oracle(prefix + b"A"*(blocksize-1-(cnt%blocksize)+ blocksize*pre_block_size-len(prefix)) + plain, key, False)
        cipher = encrypted[index*blocksize: (index+1)*blocksize]
        try:
            for c in string.printable:
                if encryption_oracle(my_prefix+c.encode(), key, False)[0][:blocksize] == cipher:
                    ans_c = c
                    break
            ans += ans_c.encode()
            cnt += 1
        except:
            break
    print(plain)
    print(ans)