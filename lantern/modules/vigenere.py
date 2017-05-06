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
        key = build_key(decrypt.key for decrypt in column_decryptions)
        period_decryptions.append(Decryption(plaintext, key, score(plaintext, score_functions)))

    return sorted(period_decryptions, reverse=True)


# Name should be different, say youre finding key periods through IC.
def key_periods(ciphertext, max_key_period):
    key_scores = []
    for period in range(1, max_key_period + 1):
        cols = split_columns(ciphertext, period)
        score = abs(ENGLISH_IC - avg_index_of_coincidence(cols))
        key_scores.append((period, score))

    return sorted(key_scores, key=lambda x: x[1])


def build_key(keys):
    return ''.join([string.ascii_uppercase[(26 - key) % 26] for key in keys])


def decrypt(key, ciphertext):
    decrypted_columns = []
    key = key.upper()

    index = 0
    for col in split_columns(ciphertext, len(key)):
        print(col)
        letter = key[index]
        shift = int(string.ascii_uppercase.index(letter))
        decrypted_columns.append(caesar.decrypt(-shift, col))
        index = (index + 1) % len(key)

    return ''.join(combine_columns(decrypted_columns))
