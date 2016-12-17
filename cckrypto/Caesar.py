from pycipher import Caesar
from .NgramScore import NgramScore
import logging

CAESER_MIN_KEY = 1
CAESER_MAX_KEY = 25

def crack(ciphertext, fitness):
    decryptions = list()
    for key in range(CAESER_MIN_KEY, CAESER_MAX_KEY + 1):
        plaintext = Caesar(key).decipher(ciphertext, True)
        rank = (plaintext, fitness.score(plaintext))
        decryptions.append(rank)

    # Sort based on best score
    decryptions = sorted(decryptions, key=lambda x: x[1], reverse=True)
    map(logging.debug, decryptions)

    # Return best decryption
    return decryptions[0][0]
