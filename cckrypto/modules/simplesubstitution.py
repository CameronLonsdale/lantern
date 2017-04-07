"""Automated breaking of the Simple Substitution cipher"""
import random
import string

from cckrypto.score import score


def _decipher(key, ciphertext):
    rev_map = {v: k for k, v in zip(key, string.ascii_uppercase)}
    return ''.join((rev_map[char] if char in rev_map else char for char in ciphertext))


def crack(ciphertext, score_functions, nswaps=3000, ntrials=30):
    ciphertext = ciphertext.upper()
    key = list(string.ascii_uppercase)
    decryptions = []
    best_score = -99e9  # TODO: I Don't like this magic number

    # Find global maximums
    for iteration in range(ntrials):
        random.shuffle(key)
        best_trial_score = -99e9

        for swap in range(nswaps):
            new_key = key[:]

            # Swap 2 characters in the key
            a, b = random.sample(range(26), 2)  # TODO: More magic numbers :(
            new_key[a], new_key[b] = new_key[b], new_key[a]

            plaintext = _decipher(new_key, ciphertext)
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
                (_decipher(best_key, ciphertext), best_score)
            )

    return sorted(decryptions, key=lambda x: x[1], reverse=True)
