#!/usr/bin/env python3

from lantern.modules import atbash

ciphertext = "uozt{Yzybolm}"
print(''.join(atbash.decrypt(ciphertext)))
