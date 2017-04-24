"""Automated breaking of the Caesar cipher."""
import string

from lantern.score import score
from lantern.decryption import Decryption

MIN_KEY = 0
MAX_KEY = 26


def _decrypt(key, ciphertext):
    shifted = string.ascii_uppercase[key:] + string.ascii_uppercase[:key]
    rev_map = {v: k for k, v in zip(shifted, string.ascii_uppercase)}
    return ''.join((rev_map[char] if char in rev_map else char for char in ciphertext))


def crack(ciphertext, score_functions):
    """Break Casear cipher encryption by enumeration all keys in the keyspace."""
    decryptions = []
    ciphertext = ciphertext.upper()

    for key in range(MIN_KEY, MAX_KEY):
        plaintext = _decrypt(key, ciphertext)
        decryption = Decryption(plaintext, key, score(plaintext, score_functions))
        decryptions.append(decryption)

    return sorted(decryptions, key=lambda x: x.score, reverse=True)
