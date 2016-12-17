from pycipher import Caesar
from .NgramScore import NgramScore
from .util import remove_punctuation
import logging

MIN_KEY = 1
MAX_KEY = 25

def crack(ciphertext, fitness):
    decryptions = list()
    for key in range(MIN_KEY, MAX_KEY + 1):
        plaintext = Caesar(key).decipher(ciphertext, True)
        # score with no punctuation gives best results
        rank = (plaintext, fitness.score(remove_punctuation(plaintext)))
        decryptions.append(rank)

    # Sort based on best score
    decryptions = sorted(decryptions, key=lambda x: x[1], reverse=True)
    map(logging.debug, decryptions)

    # Return best decryption
    return decryptions[0][0]
