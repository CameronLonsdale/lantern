"""Tests for the Decryption Structure"""

from lantern.structures import Decryption


def test_kwargs():
    """test kwargs builds properly"""
    decryption = Decryption(plaintext="plaintext", score=0, key="key")
    assert decryption.plaintext == "plaintext"
    assert decryption.score == 0
    assert decryption.key == "key"


def test_args():
    """test args builds properly"""
    decryption = Decryption("plaintext", "key", 0)
    assert decryption.plaintext == "plaintext"
    assert decryption.key == "key"
    assert decryption.score == 0


def test_str():
    """test string typecast returns plaintext"""
    decryption = Decryption("plaintext", "key", 0)
    assert str(decryption) == "plaintext"


def test_lt():
    """test __lt__ compares using score"""
    decryption1 = Decryption("plaintext1", "key1", 0)
    decryption2 = Decryption("plaintext2", "key2", -1)
    assert decryption2 < decryption1
