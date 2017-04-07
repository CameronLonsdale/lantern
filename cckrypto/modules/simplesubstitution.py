"""Automated breaking of the Simple Substitution cipher"""
import random
import math
import string

from pycipher import SimpleSubstitution
from cckrypto.score import score


def crack(ciphertext, score_functions, nswaps=3000, ntrials=30):
    key = list(string.ascii_lowercase)
    decryptions = []
    best_score = -99e9

    # Find global maximums
    for iteration in range(ntrials):
        random.shuffle(key)
        best_trial_score = -99e9

        for swap in range(nswaps):
            new_key = key[:]

            # Swap 2 characters in the key
            a, b = random.sample(range(26), 2)
            new_key[a], new_key[b] = new_key[b], new_key[a]

            plaintext = SimpleSubstitution(new_key).decipher(ciphertext, keep_punct=True)
            new_score = score(plaintext, score_functions)

            # Keep track of best score for a single trial
            if new_score > best_trial_score:
                key = new_key[:]
                best_trial_score = new_score

        # Keep track of the best score over all trials
        if best_trial_score > best_score:
            best_key = key[:]
            best_score = best_trial_score
            decryptions.append(
                (SimpleSubstitution(best_key).decipher(ciphertext, keep_punct=True), best_score)
            )

    return sorted(decryptions, key=lambda x: x[1], reverse=True)
