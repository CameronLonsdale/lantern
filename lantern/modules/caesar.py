"""Automated breaking of the Caesar cipher."""
from pycipher import Caesar
from lantern.score import score

MIN_KEY = 1
MAX_KEY = 25


def crack(ciphertext, score_functions):
    """Break Casear cipher encryption by enumeration all keys in the keyspace."""
    decryptions = []

    for key in range(MIN_KEY, MAX_KEY + 1):
        plaintext = Caesar(key).decipher(ciphertext, keep_punct=True)

        decryption = (plaintext, score(plaintext, score_functions))
        decryptions.append(decryption)

    # Sort based on best score
    return sorted(decryptions, key=lambda x: x[1], reverse=True)
