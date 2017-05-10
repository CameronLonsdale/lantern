"""Automated breaking of the Vigenere Cipher"""

import string

import itertools

from lantern import score
from lantern.modules import caesar
from lantern.structures import Decryption

from lantern.analysis.frequency import (
    avg_index_of_coincidence, ENGLISH_IC
)

from lantern.util import (
    split_columns, combine_columns
)


# TODO: maybe add finding keyperiods as a parameter because people might want to use kasiski
def crack(ciphertext, score_functions, key_period=None, max_key_period=30):
    """
    Break ``ciphertext`` by finding (or using the given) key_period then breaking 
    ``key_period`` many Caesar ciphers.

    Example: ::

        crack(ciphertext, fitness.ChiSquared(analysis.frequency.english.unigrams)

    :param str ciphertext: The text to decrypt
    :param scoring_functions: Function(s) to score decryptions with
    :param int key_period: The period of the key
    :param int max_key_period: The maximum period the key could be
    :return: Sorted list of decryptions
    :raises ValueError: If ``key_period`` or ``max_key_period`` are less than or equal to 0
    """
    if max_key_period <= 0 or (key_period is not None and key_period <= 0):
        raise ValueError("Period values must be positive integers")

    if key_period is None:
        periods = key_periods(ciphertext, max_key_period)
    else:
        periods = [(int(key_period), 0)]

    period_decryptions = []
    for period, _ in filter(lambda p: p[0] <= len(ciphertext), periods):
        column_decryptions = []
        for col in split_columns(ciphertext, period):
            decryptions = caesar.crack(col, score_functions)
            column_decryptions.append(decryptions[0])

        plaintext = combine_columns(decrypt.plaintext for decrypt in column_decryptions)
        key = _build_key(decrypt.key for decrypt in column_decryptions)
        period_decryptions.append(Decryption(plaintext, key, score(plaintext, score_functions)))

    return sorted(period_decryptions, reverse=True)


# Name should be different?, say youre finding key periods through IC.
def key_periods(ciphertext, max_key_period):
    """
    Rank all key periods for ``ciphertext`` up to and including ``max_key_period``

    Example: ::

        key_periods(ciphertext, 30)

    :param str ciphertext: The text to analyze
    :param int max_key_period: The maximum period the key could be
    :return: Sorted list of keys, ordered from most likely to least likely
    :raises ValueError: If max_key_period is less than or equal to 0
    """
    if max_key_period <= 0:
        raise ValueError("max_key_period must be a positive integer")

    key_scores = []
    for period in range(1, max_key_period + 1):
        cols = split_columns(ciphertext, period)
        score = abs(ENGLISH_IC - avg_index_of_coincidence(cols))
        key_scores.append((period, score))

    return sorted(key_scores, key=lambda x: x[1])


def _build_key(keys):
    return ''.join([string.ascii_uppercase[(26 - key) % 26] for key in keys])


def decrypt(key, ciphertext):
    """
    Decrypt Vigenere encrypted ``ciphertext`` using ``key``.

    Example: ::

        decrypt("KEY", "RIJVS") == "HELLO"

    :param iterable key: The key to use
    :param str ciphertext: The text to decrypt
    :return: plaintext
    """
    decrypted_columns = []
    key = ''.join(key).upper()

    index = 0
    for col in split_columns(ciphertext, len(key)):
        print(col)
        letter = key[index]
        shift = int(string.ascii_uppercase.index(letter))
        decrypted_columns.append(caesar.decrypt(shift, col))
        index = (index + 1) % len(key)

    return ''.join(combine_columns(decrypted_columns))
