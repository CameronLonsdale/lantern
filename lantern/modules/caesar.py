"""Automated breaking of the Caesar cipher."""
import string

from lantern import score
from lantern.structures import Decryption


def crack(ciphertext, score_functions, min_key=0, max_key=26):
    """Break Casear cipher encryption by enumeration all keys in the keyspace."""
    decryptions = []

    for key in range(min_key, max_key):
        plaintext = decrypt(key, ciphertext)
        decryption = Decryption(plaintext, key, score(plaintext, score_functions))
        decryptions.append(decryption)

    return sorted(decryptions, reverse=True)


# TODO:
# make decrypt a colsure which decrypts based on a certain source language
# because right now it is hard coded to english
def decrypt(key, ciphertext):
    alphabet = string.ascii_letters
    shifted_lower = string.ascii_lowercase[key:] + string.ascii_lowercase[:key]
    shifted_upper = string.ascii_uppercase[key:] + string.ascii_uppercase[:key]
    shifted = shifted_lower + shifted_upper

    try:
        table = str.maketrans(alphabet, shifted)
    except AttributeError:
        table = string.maketrans(alphabet, shifted)
    return ciphertext.translate(table)
