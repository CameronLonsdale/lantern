"""Automated breaking of the Caesar cipher."""
import string

from lantern import score
from lantern.structures import Decryption


def crack(ciphertext, score_functions, min_key=0, max_key=26):
    """
    Break ``ciphertext`` by enumeration keys between ``min_key`` and ``max_key``.

    Example: ::

        crack(ciphertext, fitness.english.quadgrams)

    :param str ciphertext: The text to decrypt
    :param scoring_functions: Function(s) to score text with
    :param int min_key: Key to start with
    :param int max_key: Key to stop at
    :type scoring_functions: Function or iterable of functions
    :return: Sorted list of decryptions
    :raises ValueError: If min_key exceeds max_key
    """
    if min_key >= max_key:
        raise ValueError("min_key cannot exceed max_key")

    decryptions = []

    for key in range(min_key, max_key):
        plaintext = decrypt(key, ciphertext)
        decryption = Decryption(plaintext, key, score(plaintext, score_functions))
        decryptions.append(decryption)

    return sorted(decryptions, reverse=True)


# TODO:
# make decrypt a closure which decrypts based on a certain source language
# because right now it is hard coded to english

def decrypt(key, ciphertext):
    """
    Decrypt Caesar encrypted ``ciphertext`` using ``key``.

    Example: ::

        decrypt(3, "KHOOR") == "HELLO"

    :param int key: The shift to use
    :param str ciphertext: The text to decrypt
    :return: plaintext
    """
    alphabet = string.ascii_letters
    key %= len(string.ascii_lowercase)
    shifted_lower = string.ascii_lowercase[key:] + string.ascii_lowercase[:key]
    shifted_upper = string.ascii_uppercase[key:] + string.ascii_uppercase[:key]
    shifted = shifted_lower + shifted_upper

    try:
        table = str.maketrans(shifted, alphabet)
    except AttributeError:
        table = string.maketrans(shifted, alphabet)
    return ciphertext.translate(table)
