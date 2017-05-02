#!/usr/bin/python

from lantern.modules import caesar
from lantern import fitness

ciphertext = "iodj{EuxwhIrufhLvEhvwIrufh}"

decryptions = caesar.crack(ciphertext, fitness.english.quadgrams)
print(decryptions[0])
