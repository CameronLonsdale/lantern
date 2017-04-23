from lantern.modules import caesar
from lantern.score_functions import ngram

ciphertext = """iodj{EuxwhIrufhLvEhvwIrufh}"""

print(caesar.crack(ciphertext, [ngram.quadgram()])[0])
