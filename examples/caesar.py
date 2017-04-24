from lantern.modules import caesar
from lantern.score_functions import ngram

ciphertext = """iodj{EuxwhIrufhLvEhvwIrufh}"""

decryptions = caesar.crack(ciphertext, [ngram.quadgram()])
best_decryption = decryptions[0]
print(best_decryption.plaintext)
