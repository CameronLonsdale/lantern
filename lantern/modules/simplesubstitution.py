"""Automated breaking of the Simple Substitution Cipher."""

import random
import string

import lantern
from lantern.structures import Decryption


def crack(ciphertext, *fitness_functions, ntrials=30, nswaps=3000):
    """Break ``ciphertext`` using hill climbing.

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

    # Find a local maximum by swapping two letters and scoring the decryption
    def next_node_inner_climb(node):
        # Swap 2 characters in the key
        a, b = random.sample(range(len(node)), 2)
        node[a], node[b] = node[b], node[a]
        plaintext = decrypt(node, ciphertext)
        score = lantern.score(plaintext, *fitness_functions)
        return node, score, Decryption(plaintext, ''.join(node), score)

    # Outer climb rereuns hill climb ntrials number of times each time at a different start location
    def next_node_outer_climb(node):
        random.shuffle(node)
        key, score, outputs = hill_climb(nswaps, node[:], next_node_inner_climb)
        return key, score, outputs[-1]  # The last item in this list is the item with the highest score

    _, _, decryptions = hill_climb(ntrials, list(string.ascii_uppercase), next_node_outer_climb)
    return sorted(decryptions, reverse=True)  # We sort the list to ensure the best results are at the front of the list


def hill_climb(nsteps, start_node, get_next_node):
    """Hill climb"""
    outputs = []
    best_score = -float('inf')

    for step in range(nsteps):
        next_node, score, output = get_next_node(start_node[:])

        # Keep track of best score and the start node becomes finish node
        if score > best_score:
            start_node = next_node[:]
            best_score = score
            outputs.append(output)

    return start_node, best_score, outputs


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
