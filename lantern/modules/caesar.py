"""Automated breaking of the Caesar Cipher."""

import string

from lantern import score
from lantern.structures import Decryption


def crack(ciphertext, score_functions, min_key=0, max_key=26):
    """
    Break ``ciphertext`` by enumerating keys between ``min_key`` and ``max_key``.

    Example: ::

        crack(ciphertext, fitness.english.quadgrams)

    Parameters:
        ciphertext (str): The text to decrypt
        scoring_functions (Function or iterable of functions): Function(s) to score decryptions with
        min_key (int): Key to start with
        max_key (int): Key to stop at (exclusive)

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
    alphabet = [string.ascii_lowercase, string.ascii_uppercase]
    key %= len(alphabet[0])
    shifted = _shift_alphabet(alphabet, key)
    return ciphertext.translate(str.maketrans(''.join(shifted), ''.join(alphabet)))


def _shift_alphabet(letter_cases, shift):
    return [case[shift:] + case[:shift] for case in letter_cases]
