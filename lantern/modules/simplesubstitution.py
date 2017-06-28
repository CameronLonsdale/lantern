"""Automated breaking of the Simple Substitution Cipher."""

import random
import string

from lantern import score
from lantern.analysis.search import hill_climb
from lantern.structures import Decryption


def crack(ciphertext, *fitness_functions, ntrials=30, nswaps=3000):
    """Break ``ciphertext`` using hill climbing.

    Note:
        Currently ntrails and nswaps default to magic numbers.
        Generally the trend is, the longer the text, the lower the number of trials
        you need to run, because the hill climbing will lead to the best answer faster.
        Because randomness is involved, there is the possibility of the correct decryption
        not being found. In this circumstance you just need to run the code again.

    Example:
        >>> decryptions = crack("XUOOB", fitness.english.quadgrams)
        >>> print(decryptions[0])
        HELLO

    Args:
        ciphertext (str): The text to decrypt
        *fitness_functions (variable length argument list): Functions to score decryption with

    Keyword Args:
        ntrials (int): The number of times to run the hill climbing algorithm
        nswaps (int): The number of rounds to find a local maximum

    Returns:
        Sorted list of decryptions

    Raises:
        ValueError: If nswaps or ntrails are not positive integers
        ValueError: If no fitness_functions are given
    """
    if ntrials <= 0 or nswaps <= 0:
        raise ValueError("ntrials and nswaps must be positive integers")

    # Find a local maximum by swapping two letters and scoring the decryption
    def next_node_inner_climb(node):
        # Swap 2 characters in the key
        a, b = random.sample(range(len(node)), 2)
        node[a], node[b] = node[b], node[a]
        plaintext = decrypt(node, ciphertext)
        node_score = score(plaintext, *fitness_functions)
        return node, node_score, Decryption(plaintext, ''.join(node), node_score)

    # Outer climb rereuns hill climb ntrials number of times each time at a different start location
    def next_node_outer_climb(node):
        random.shuffle(node)
        key, best_score, outputs = hill_climb(nswaps, node[:], next_node_inner_climb)
        return key, best_score, outputs[-1]  # The last item in this list is the item with the highest score

    _, _, decryptions = hill_climb(ntrials, list(string.ascii_uppercase), next_node_outer_climb)
    return sorted(decryptions, reverse=True)  # We sort the list to ensure the best results are at the front of the list


def decrypt(key, ciphertext):
    """Decrypt Simple Substitution enciphered ``ciphertext`` using ``key``.

    Example:
        >>> decrypt("PQSTUVWXYZCODEBRAKINGFHJLM", "XUOOB")
        HELLO

    Args:
        key (iterable): The key to use
        ciphertext (str): The text to decrypt

    Returns:
        Decrypted ciphertext
    """
    # TODO: Is it worth keeping this here I should I only accept strings?
    key = ''.join(key)
    alphabet = string.ascii_letters
    cipher_alphabet = key.lower() + key.upper()
    return ciphertext.translate(str.maketrans(cipher_alphabet, alphabet))
