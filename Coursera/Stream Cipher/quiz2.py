s = "learn wisdom by the follies of others."
ans = ""
for c in s:
    if c!=' ' and c!='.':
        print(chr((ord(c)-ord('a')+7)%26+ord('a')),end='')
        ans+=chr((ord(c)-ord('a')+7)%26+ord('a'))
    else:
        print(c,end='')
        ans+=c
print()
print(ans.upper())