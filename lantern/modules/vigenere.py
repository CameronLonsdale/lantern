from collections import defaultdict

from lantern.modules import caesar
from lantern.analysis import avg_index_of_coincidence, ENGLISH_IC
from lantern.structures import Decryption


# TODO: maybe add finding keyperiods as a parameter because people might want to use kasiski
def crack(ciphertext, score_functions, max_key_period):
    periods = key_periods(ciphertext, max_key_period)
    best_period = periods[0][0]

    column_decryptions = []
    best_decryptions = []
    for col in break_columns(ciphertext, best_period):
        decryptions = caesar.crack(col, score_functions)
        column_decryptions.append(decryptions)
        best_decryptions.append(decryptions[0].plaintext)

    return Decryption(combine_columns(best_decryptions), "need key", 0)


def break_columns(ciphertext, key_length):
    return [ciphertext[i::key_length] for i in range(key_length)]


def combine_columns(columns):
    return ''.join(x for zipped in zip(*columns) for x in zipped)


# Name should be different, say youre finding key periods through IC.
def key_periods(ciphertext, max_key_period):
    key_scores = []
    for period in range(1, max_key_period + 1):
        cols = break_columns(ciphertext, period)
        score = abs(ENGLISH_IC - avg_index_of_coincidence(cols))
        key_scores.append((period, score))

    return sorted(key_scores, key=lambda x: x[1])