"""Automated breaking of the Vigenere Cipher."""

import string

from lantern import score
from lantern.modules import caesar
from lantern.structures import Decryption

from lantern.analysis.frequency import index_of_coincidence, ENGLISH_IC
from lantern.util import split_columns, remove


# TODO: maybe add finding keyperiods as a parameter because people might want to use kasiski
def crack(ciphertext, *fitness_functions, key_period=None, max_key_period=30):
    """
    Break ``ciphertext`` by finding (or using the given) key_period then breaking ``key_period`` many Caesar ciphers.

    Example: ::

        crack(ciphertext, fitness.ChiSquared(analysis.frequency.english.unigrams))

    Arguments:
        ciphertext (str): The text to decrypt
        fitness_functions (variable length arg list): Functions to score decryption with

    Keyword Arguments:
        key_period (int): The period of the key
        max_key_period (int): The maximum period the key could be

    Return:
        Sorted list of decryptions

    Raises:
        ValueError: If key_period or max_key_period are less than or equal to 0
    """
    if max_key_period <= 0 or (key_period is not None and key_period <= 0):
        raise ValueError("Period values must be positive integers")

    original_text = ciphertext
    ciphertext = remove(ciphertext, string.punctuation + string.whitespace)
    periods = [int(key_period)] if key_period else key_periods(ciphertext, max_key_period)

    period_decryptions = []
    for period in filter(lambda p: p <= len(ciphertext), periods):
        column_decryptions = []
        for col in split_columns(ciphertext, period):
            decryptions = caesar.crack(col, *fitness_functions)
            column_decryptions.append(decryptions[0])

        key = _build_key(decrypt.key for decrypt in column_decryptions)
        plaintext = decrypt(key, original_text)
        period_decryptions.append(Decryption(plaintext, key, score(plaintext, *fitness_functions)))

    return sorted(period_decryptions, reverse=True)


# Name should be different?, say youre finding key periods through IC.
def key_periods(ciphertext, max_key_period):
    """
    Rank all key periods for ``ciphertext`` up to and including ``max_key_period``

    Example: ::

        key_periods(ciphertext, 30)

    Parameters:
        ciphertext (str): The text to analyze
        max_key_period (int): The maximum period the key could be

    Return:
        Sorted list of keys

    Raises:
        ValueError: If max_key_period is less than or equal to 0
    """
    if max_key_period <= 0:
        raise ValueError("max_key_period must be a positive integer")

    key_scores = []
    for period in range(1, max_key_period + 1):
        cols = split_columns(ciphertext, period)
        score = abs(ENGLISH_IC - index_of_coincidence(*cols))
        key_scores.append((period, score))

    return [p[0] for p in sorted(key_scores, key=lambda x: x[1])]


def _build_key(keys):
    return ''.join([string.ascii_uppercase[(key) % 26] for key in keys])


def decrypt(key, ciphertext):
    """
    Decrypt Vigenere encrypted ``ciphertext`` using ``key``.

    Example: ::

        decrypt("KEY", "RIJVS") == "HELLO"

    Parameters:
        key (iterable): The key to use
        ciphertext (str): The text to decrypt

    Return:
        plaintext
    """
    decrypted = ""
    key = ''.join(key)

    index = 0
    for char in ciphertext:
        if char not in string.punctuation + string.whitespace:
            alphabet = string.ascii_uppercase if key[index].isupper() else string.ascii_lowercase
            char = caesar.decrypt(int(alphabet.index(key[index])), char)
            index = (index + 1) % len(key)
        decrypted += char

    return ''.join(decrypted)
