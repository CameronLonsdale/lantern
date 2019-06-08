#!/usr/bin/env python3

from lantern.modules import shift
from lantern import fitness

ciphertext = "iodj{EuxwhIrufhLvEhvwIrufh}"

decryptions = shift.crack(ciphertext, fitness.english.quadgrams)
print(''.join(decryptions[0].plaintext))
