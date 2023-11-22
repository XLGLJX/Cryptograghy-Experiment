from Crypto.Util.strxor import strxor
s1 = "1c0111001f010100061a024b53535009181c"
s2 = "686974207468652062756c6c277320657965"
ans = strxor(bytes.fromhex(s1),bytes.fromhex(s2))
print(ans)
print(ans.hex())