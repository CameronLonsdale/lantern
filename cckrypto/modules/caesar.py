"""Automated breaking of the Caesar cipher."""
from pycipher import Caesar
from cckrypto.util import remove_punctuation

MIN_KEY = 1
MAX_KEY = 25


def crack(ciphertext, fitness):
    """Return ordered decryptions."""
    decryptions = list()
    for key in range(MIN_KEY, MAX_KEY + 1):
        plaintext = Caesar(key).decipher(ciphertext, keep_punct=True)
        rank = (plaintext, fitness.score(remove_punctuation(plaintext)))
        decryptions.append(rank)

    # Sort based on best score
    return sorted(decryptions, key=lambda x: x[1], reverse=True)
