from oracle import *
import sys
import Crypto.Cipher.AES as aes

size = 16

data = "9F0B13944841A832B2421B9EAF6D9836813EC9D944A5C8347A7CA69AA34D8DC0DF70E343C4000A2AE35874CE75E64C31"
# c = bytes.fromhex(c)
# print(c)

ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]

Oracle_Connect()
rc = Oracle_Send(ctext, 3)
print("Oracle returned: %d" % rc)
Oracle_Disconnect()

