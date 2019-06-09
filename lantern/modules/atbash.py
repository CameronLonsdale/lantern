"""Automated breaking of the Atbash Cipher."""

from lantern.modules import simplesubstitution

from typing import Iterable

# TODO: Consider using an affine cipher for transformation in future

KEY = 'ZYXWVUTSRQPONMLKJIHGFEDCBA'


def decrypt(ciphertext: str) -> Iterable:
    """Decrypt Atbash enciphered ``ciphertext``.

    Examples:
        >>> ''.join(decrypt("SVOOL"))
        HELLO

    Args:
        ciphertext (str): English string to decrypt

    Returns:
        Decrypted text
    """
    return simplesubstitution.decrypt(KEY, ciphertext)


def encrypt(plaintext: str) -> Iterable:
    """Encrypt ``plaintext`` using the Atbash cipher.

    Examples:
        >>> ''.join(encrypt("HELLO"))
        SVOOL

    Args:
        plaintext (str): English string to encrypt

    Returns:
        Encrypted text
    """
    return simplesubstitution.encrypt(KEY, plaintext)
