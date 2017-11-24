"""Automated breaking of the Shift Cipher."""

import string

from lantern import score
from lantern.structures import Decryption


def make_shift_function(alphabet):
    """Construct a shift function from an alphabet.

    Examples:
        Shift cases independently

        >>> make_shift_function([string.ascii_uppercase, string.ascii_lowercase])
        <function make_shift_function.<locals>.shift_case_sensitive>

        Additionally shift punctuation characters

        >>> make_shift_function([string.ascii_uppercase, string.ascii_lowercase, string.punctuation])
        <function make_shift_function.<locals>.shift_case_sensitive>

        Shift entire ASCII range, overflowing cases

        >>> make_shift_function([''.join(chr(x) for x in range(32, 127))])
        <function make_shift_function.<locals>.shift_case_sensitive>

    Args:
        alphabet (iterable): Ordered iterable of strings representing separate cases of an alphabet

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
        >>> print(''.join(decryptions[0].plaintext))
        HELLO

    Args:
        ciphertext (iterable): The symbols to decrypt
        *fitness_functions (variable length argument list): Functions to score decryption with

    Keyword Args:
        min_key (int): Key to start with
        max_key (int): Key to stop at (exclusive)
        shift_function (function(shift, symbol)): Shift function to use

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
        plaintext = decrypt(key, ciphertext, shift_function=shift_function)
        decryptions.append(Decryption(plaintext, key, score(plaintext, *fitness_functions)))

    return sorted(decryptions, reverse=True)


def decrypt(key, ciphertext, shift_function=shift_case_english):
    """Decrypt Shift enciphered ``ciphertext`` using ``key``.

    Examples:
        >>> ''.join(decrypt(3, "KHOOR"))
        HELLO

        >> decrypt(15, [0xcf, 0x9e, 0xaf, 0xe0], shift_bytes)
        [0xde, 0xad, 0xbe, 0xef]

    Args:
        key (int): The shift to use
        ciphertext (iterable): The symbols to decrypt
        shift_function (function (shift, symbol)): Shift function to apply to symbols in the ciphertext

    Returns:
        Decrypted ciphertext, list of plaintext symbols
    """
    return [shift_function(key, symbol) for symbol in ciphertext]
