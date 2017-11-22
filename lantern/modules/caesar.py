"""Automated breaking of the Caesar Cipher."""

import string

from lantern import score
from lantern.structures import Decryption


def make_shift_function(alphabet):
    """Construct a shift function from an alphabet.

    Examples:
        Shift cases independently

        >>> make_shift_function([string.ascii_uppercase, string.ascii_lowercase])

        Additionally shift punctuation characters

        >>> make_shift_function([string.ascii_uppercase, string.ascii_lowercase, string.punctuation])

        Shift entire ascii range, overflowing cases

        >>> make_shift_function([''.join(chr(x) for x in range(32, 127))])

    Args:
        alphabet (iterable): Ordered iterable of strings representing separated cases of an alphabet

    Returns:
        Function (shift, symbol)

    """
    def shift_case_sensitive(shift, symbol):
        case = [case for case in alphabet if symbol in case]
        if not case:
            return symbol

        case = case[0]
        index = case.index(symbol)
        return case[(index - shift) % len(case)]

    return shift_case_sensitive

shift_case_english = make_shift_function([string.ascii_uppercase, string.ascii_lowercase])


def crack(ciphertext, *fitness_functions, min_key=0, max_key=26, shift_function=shift_case_english):
    """Break ``ciphertext`` by enumerating keys between ``min_key`` and ``max_key``.

    Example:
        >>> decryptions = crack("KHOOR", fitness.english.quadgrams)
        >>> print(decryptions[0])
        HELLO

    Args:
        ciphertext (str): The text to decrypt
        *fitness_functions (variable length argument list): Functions to score decryption with

    Keyword Args:
        min_key (int): Key to start with
        max_key (int): Key to stop at (exclusive)

    Returns:
        Sorted list of decryptions

    Raises:
        ValueError: If min_key exceeds max_key
        ValueError: If no fitness_functions are given
    """
    if min_key >= max_key:
        raise ValueError("min_key cannot exceed max_key")

    decryptions = []
    for key in range(min_key, max_key):
        plaintext = ''.join(decrypt(key, ciphertext, shift_function=shift_function))
        decryptions.append(Decryption(plaintext, key, score(plaintext, *fitness_functions)))

    return sorted(decryptions, reverse=True)


def decrypt(key, ciphertext, shift_function=shift_case_english):
    """Decrypt Caesar enciphered ``ciphertext`` using ``key``.

    Example:
        >>> decrypt(3, "KHOOR")
        HELLO

    Args:
        key (int): The shift to use
        ciphertext (str): The text to decrypt

    Keyword Args:
        shift_function (function (shift, symbol)): shift function to apply to symbols in the ciphertext

    Returns:
        Decrypted ciphertext
    """
    return [shift_function(key, symbol) for symbol in ciphertext]
