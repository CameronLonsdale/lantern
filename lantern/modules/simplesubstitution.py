"""Automated breaking of the Simple Substitution cipher"""
import random
import string

from lantern import score
from lantern.structures import Decryption


def crack(ciphertext, score_functions, ntrials=30, nswaps=3000):
    key = list(string.ascii_uppercase)
    decryptions = []
    best_score = -float('inf')

    # Find global maximums
    for iteration in range(ntrials):
        random.shuffle(key)
        best_trial_score = -float('inf')

        for swap in range(nswaps):
            new_key = key[:]

            # Swap 2 characters in the key
            a, b = random.sample(range(26), 2)
            new_key[a], new_key[b] = new_key[b], new_key[a]

            plaintext = decrypt(new_key, ciphertext)
            new_score = score(plaintext, score_functions)

            # Keep track of best score for a single trial
            if new_score > best_trial_score:
                key = new_key[:]
                best_trial_score = new_score

        # Keep track of the best score over all trials
        if best_trial_score > best_score:
            best_key = key[:]
            best_score = best_trial_score
            decryption = Decryption(decrypt(best_key, ciphertext), ''.join(best_key), best_score)
            decryptions.append(decryption)

    return sorted(decryptions, reverse=True)


def decrypt(key, ciphertext):
    key = ''.join(key)
    alphabet = string.ascii_letters
    reversed_alphabet = key.lower() + key.upper()

    try:
        table = str.maketrans(reversed_alphabet, alphabet)
    except AttributeError:
        table = string.maketrans(reversed_alphabet, alphabet)
    return ciphertext.translate(table)
