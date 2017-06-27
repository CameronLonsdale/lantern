"""Automated breaking of the Simple Substitution Cipher."""

import random
import string

import lantern
from lantern.structures import Decryption


def crack(ciphertext, *fitness_functions, ntrials=30, nswaps=3000):
    """Break ``ciphertext`` using a hill climbing algorithm.

    Example:
        >>> decryptions = crack("XUOOB", fitness.english.quadgrams)
        >>> print(decryptions[0])
        HELLO

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

    def get_next_node(node):
        # Swap 2 characters in the key
        a, b = random.sample(range(len(node)), 2)
        node[a], node[b] = node[b], node[a]
        return node, lantern.score(decrypt(node, ciphertext), *fitness_functions)

    # Repeat hill climb at different starting points for more comprehensive results
    for iteration in range(ntrials):
        random.shuffle(key)
        score, key = hill_climb(nswaps, key[:], get_next_node)

        # Keep track of the best score over all trials
        if score > best_score:
            best_key = key[:]
            best_score = score
            decryptions.append(Decryption(decrypt(best_key, ciphertext), ''.join(best_key), best_score))

    return sorted(decryptions, reverse=True)


def hill_climb(nsteps, start_node, get_next_node):
    best_score = -float('inf')
    for step in range(nsteps):
        next_node, score = get_next_node(start_node[:])

        # Keep track of best score and the start node becomes finish node
        if score > best_score:
            start_node = next_node[:]
            best_score = score

    return best_score, start_node


def decrypt(key, ciphertext):
    """Decrypt Simple Substitution enciphered ``ciphertext`` using ``key``.

    Example:
        >>> decrypt("PQSTUVWXYZCODEBRAKINGFHJLM", "XUOOB")
        HELLO

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
