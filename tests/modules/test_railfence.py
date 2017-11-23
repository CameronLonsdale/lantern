"""Tests for the Railfence module"""

import pycipher
import string

import pytest
from tests.util import get_top_decryptions

from lantern.modules import railfence
from lantern import fitness


def _test_railfence(plaintext, *fitness_functions, key=3, top_n=1):
    ciphertext = pycipher.Railfence(key).encipher(plaintext, keep_punct=True)
    decryptions = railfence.crack(ciphertext, *fitness_functions)

    top_decryptions = get_top_decryptions(decryptions, top_n)

    match = None
    for decrypt in top_decryptions:
        if decrypt.plaintext.upper() == plaintext.upper():
            match = decrypt
            break

    assert match is not None
    assert match.key == key


def test_example_unigrams():
    """Testing quick brown fox"""
    plaintext = "Thisisanexample"
    _test_railfence(plaintext, fitness.english.quadgrams)
