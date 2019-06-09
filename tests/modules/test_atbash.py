"""Tests for the Caeser module"""

import pycipher

from lantern.modules import atbash


def _test_atbash(plaintext, *fitness_functions, top_n=1):
    ciphertext = pycipher.Atbash().encipher(plaintext, keep_punct=True)
    decryption = atbash.decrypt(ciphertext)

    assert decryption == plaintext.upper()


def test_decrypt():
    """Test decryption"""
    assert atbash.decrypt("uozt{Yzybolm}") == "flag{Babylon}"


def test_encrypt():
    """Test encrypt"""
    assert ''.join(atbash.encrypt("flag{Babylon}")) == "uozt{Yzybolm}"
