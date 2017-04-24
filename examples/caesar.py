#!/usr/bin/python

from lantern.modules import caesar
from lantern.score_functions import english_scorer

ciphertext = """iodj{EuxwhIrufhLvEhvwIrufh}"""

decryptions = caesar.crack(ciphertext, [english_scorer.quadgrams()])
best_decryption = decryptions[0]
print(best_decryption.plaintext)
