"""Automated breaking of the Caesar Cipher"""

import string

from lantern import score
from lantern.structures import Decryption


def crack(ciphertext, score_functions, min_key=0, max_key=26):
    """
    Break ``ciphertext`` by enumeration keys between ``min_key`` and ``max_key``.

    Example: ::

        crack(ciphertext, fitness.english.quadgrams)

    Parameters:
        ciphertext (str): The text to decrypt
        scoring_functions (Function or iterable of functions): Function(s) to score decryptions with
        min_key (int): Key to start with
        max_key (int): Key to stop at

    Return:
        Sorted list of decryptions

    Raises:
        ValueError: If min_key exceeds max_key
    """
    if min_key >= max_key:
        raise ValueError("min_key cannot exceed max_key")

    decryptions = []

    for key in range(min_key, max_key):
        plaintext = decrypt(key, ciphertext)
        decryptions.append(Decryption(plaintext, key, score(plaintext, score_functions)))

    return sorted(decryptions, reverse=True)


# TODO: make decrypt a closure which decrypts based on a certain source language
# because right now it is hard coded to english
def decrypt(key, ciphertext):
    """
    Decrypt Caesar encrypted ``ciphertext`` using ``key``.

    Example: ::

        decrypt(3, "KHOOR") == "HELLO"

    Parameters:
        key (int): The shift to use
        ciphertext (str): The text to decrypt

    Return:
        plaintext
    """
    alphabet = string.ascii_letters
    key %= len(string.ascii_lowercase)
    shifted_lower = string.ascii_lowercase[key:] + string.ascii_lowercase[:key]
    shifted_upper = string.ascii_uppercase[key:] + string.ascii_uppercase[:key]
    shifted = shifted_lower + shifted_upper

    return ciphertext.translate(str.maketrans(shifted, alphabet))
