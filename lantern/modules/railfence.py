"""Automated breaking of the Railfence Cipher."""

import string

from lantern import score
from lantern.structures import Decryption


def crack(ciphertext, *fitness_functions, min_key=1, max_key=30):
    """Break ``ciphertext`` by enumerating keys between ``min_key`` and ``max_key``.

    Example:
        >>> decryptions = crack("EAPEXML", fitness.english.quadgrams)
        >>> print(decryptions[0])
        EXAMPLE

    Args:
        ciphertext (str): The text to decrypt
        *fitness_functions (variable length argument list): Functions to score decryption with

    Keyword Args:
        min_key (int): Key to start with
        max_key (int): Key to stop at (exclusive)

    Returns:
        Sorted list of decryptions

    Raises:
        ValueError: If either key is non positive
        ValueError: If min_key exceeds max_key
        ValueError: If no fitness_functions are given
    """
    if min_key >= max_key:
        raise ValueError("min_key cannot exceed max_key")

    decryptions = []
    for key in range(min_key, max(max_key, len(ciphertext))):
        plaintext = ''.join(decrypt(key, ciphertext))
        decryptions.append(Decryption(plaintext, key, score(plaintext, *fitness_functions)))

    return sorted(decryptions, reverse=True)


def decrypt(key, ciphertext):
    """Decrypt Railfence enciphered ``ciphertext`` using ``key``.

    Example:
        >>> decrypt(2, "EAPEXML")
        EXAMPLE

    Args:
        key (int): The key to use
        ciphertext (str): The text to decrypt

    Returns:
        Decrypted ciphertext
    """
    if key <= 0:
        raise ValueError("key must be positive")

    # Create a buffer representing the grid of the fenced ciphertext
    decryption = [[None] * len(ciphertext) for level in range(key)]

    rails = list(range(key - 1)) + list(range(key - 1, 0, -1))
    if not rails:
        return ciphertext

    # Fill in the spots where the characters would be with the the index of the character from the ciphertext
    for n in range(len(ciphertext)):
        decryption[rails[n % len(rails)]][n] = n

    # Condense the list into a transposition mapping
    mapping = [c for rail in decryption for c in rail if c is not None]

    # Apply the mapping to the ciphertext to place letters in the correct order
    return [ciphertext[mapping.index(n)] for n in range(len(ciphertext))]
