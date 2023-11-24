from gmpy2 import gcd, powmod
from Crypto.Util.number import *
import tqdm 

p,q = 1009,3643
n = p*q
phi = (p-1)*(q-1)
# e = 181
minn = 0xFFFFFFFF, 0
maxn = 0, 0
for e in tqdm.trange(phi):
    if gcd(e, phi) != 1:
        continue
    cnt = 0
    for m in range(n):
        if powmod(m, e, n) == m:
            cnt += 1
    if cnt < minn[0]:
        minn = cnt, e
    if cnt > maxn[0]:
        maxn = cnt, e

print(f"minn: {minn}")
print(f"maxn: {maxn}")    