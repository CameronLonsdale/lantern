"""Automated breaking of the Simple Substitution Cipher."""

import random
import string

from lantern import score
from lantern.structures import Decryption


def crack(ciphertext, *fitness_functions, ntrials=30, nswaps=3000):
    """
    Break ``ciphertext`` using a hill climbing algorithm.

    Example: ::

        crack(ciphertext, fitness.english.quadgrams)

    Arguments:
        ciphertext (str): The text to decrypt
        fitness_functions (variable length arg list): Functions to score decryption with

    Keyword Arguments:
        ntrials (int): The number of times to run the hill climbing algorithm
        nswaps (int): The number of rounds to find a local maximum

    Return:
        Sorted list of decryptions

    Raises:
        ValueError: If nswaps or ntrails are not positive integers
    """
    if ntrials <= 0 or nswaps <= 0:
        raise ValueError("ntrials and nswaps must be positive integers")

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
            new_score = score(plaintext, *fitness_functions)

            # Keep track of best score for a single trial
            if new_score > best_trial_score:
                key = new_key[:]
                best_trial_score = new_score

        # Keep track of the best score over all trials
        if best_trial_score > best_score:
            best_key = key[:]
            best_score = best_trial_score
            decryptions.append(Decryption(decrypt(best_key, ciphertext), ''.join(best_key), best_score))

    return sorted(decryptions, reverse=True)


def decrypt(key, ciphertext):
    """
    Decrypt Simple Substitution enciphered ``ciphertext`` using ``key``.

    Example: ::

        decrypt("PQSTUVWXYZCODEBRAKINGFHJLM", "XUOOB") == "HELLO"

    Parameters:
        key (iterable): The key to use
        ciphertext (str): The text to decrypt

    Return:
        plaintext
    """
    key = ''.join(key)
    alphabet = string.ascii_letters
    reversed_alphabet = key.lower() + key.upper()
    return ciphertext.translate(str.maketrans(reversed_alphabet, alphabet))
