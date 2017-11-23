"""Automated breaking of the Vigenere Cipher."""

import string

from lantern import score
from lantern.modules import shift
from lantern.structures import Decryption

from lantern.analysis.frequency import index_of_coincidence, ENGLISH_IC
from lantern.util import split_columns, remove


# TODO: maybe add finding keyperiods as a parameter because people might want to use kasiski
# TODO: Maybe consider splitting the scoring functions for columns and the whole
def crack(ciphertext, *fitness_functions, key_period=None, max_key_period=30):
    """Break ``ciphertext`` by finding (or using the given) key_period then breaking ``key_period`` many Caesar ciphers.

    Example:
        >>> decryptions = crack("OMSTV", fitness.ChiSquared(analysis.frequency.english.unigrams))
        >>> print(decryptions[0])
        HELLO

    Args:
        ciphertext (str): The text to decrypt
        *fitness_functions (variable length argument list): Functions to score decryption with

    Keyword Args:
        key_period (int): The period of the key
        max_key_period (int): The maximum period the key could be

    Returns:
        Sorted list of decryptions

    Raises:
        ValueError: If key_period or max_key_period are less than or equal to 0
        ValueError: If no fitness_functions are given
    """
    if max_key_period <= 0 or (key_period is not None and key_period <= 0):
        raise ValueError("Period values must be positive integers")

    original_text = ciphertext
    # Make the assumption that non alphabet characters have not been encrypted
    # TODO: This is fairly poor code. Once languages are a thing, there should be some nice abstractions for this stuff
    ciphertext = remove(ciphertext, string.punctuation + string.whitespace + string.digits)
    periods = [int(key_period)] if key_period else key_periods(ciphertext, max_key_period)

    # Decrypt for every valid period
    period_decryptions = []
    for period in periods:
        if period >= len(ciphertext):
            continue

        # Collect the best decryptions for every column
        column_decryptions = [shift.crack(col, *fitness_functions)[0] for col in split_columns(ciphertext, period)]
        key = _build_key(decrypt.key for decrypt in column_decryptions)

        plaintext = decrypt(key, original_text)
        period_decryptions.append(Decryption(plaintext, key, score(plaintext, *fitness_functions)))

    return sorted(period_decryptions, reverse=True)


# Name should be different?, say youre finding key periods through IC.
def key_periods(ciphertext, max_key_period):
    """Rank all key periods for ``ciphertext`` up to and including ``max_key_period``

    Example:
        >>> key_periods(ciphertext, 30)
        [2, 4, 8, 3, ...]

    Args:
        ciphertext (str): The text to analyze
        max_key_period (int): The maximum period the key could be

    Returns:
        Sorted list of keys

    Raises:
        ValueError: If max_key_period is less than or equal to 0
    """
    if max_key_period <= 0:
        raise ValueError("max_key_period must be a positive integer")

    key_scores = []
    for period in range(1, min(max_key_period, len(ciphertext)) + 1):
        score = abs(ENGLISH_IC - index_of_coincidence(*split_columns(ciphertext, period)))
        key_scores.append((period, score))

    return [p[0] for p in sorted(key_scores, key=lambda x: x[1])]


def _build_key(keys):
    num_letters = len(string.ascii_uppercase)
    return ''.join(string.ascii_uppercase[(key) % num_letters] for key in keys)


def decrypt(key, ciphertext):
    """Decrypt Vigenere encrypted ``ciphertext`` using ``key``.

    Example:
        >>> decrypt("KEY", "RIJVS")
        HELLO

    Args:
        key (iterable): The key to use
        ciphertext (str): The text to decrypt

    Returns:
        Decrypted ciphertext
    """
    index = 0
    decrypted = ""
    for char in ciphertext:
        if char in string.punctuation + string.whitespace + string.digits:
            decrypted += char
            continue  # Not part of the decryption

        # Rotate character by the alphabet position of the letter in the key
        alphabet = string.ascii_uppercase if key[index].isupper() else string.ascii_lowercase
        decrypted += ''.join(shift.decrypt(int(alphabet.index(key[index])), char))
        index = (index + 1) % len(key)

    return decrypted
