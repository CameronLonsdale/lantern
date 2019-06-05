"""Tests for the Decryption Structure"""

from lantern.structures import Decryption


def test_kwargs():
    """Testing kwargs builds properly"""
    decryption = Decryption(plaintext="plaintext", score=0, key="key")
    assert decryption.plaintext == "plaintext"
    assert decryption.score == 0
    assert decryption.key == "key"


def test_args():
    """Testing args builds properly"""
    decryption = Decryption("plaintext", "key", 0)
    assert decryption.plaintext == "plaintext"
    assert decryption.key == "key"
    assert decryption.score == 0


def test_lt():
    """Testing __lt__ compares using score"""
    decryption1 = Decryption("plaintext1", "key1", 0)
    decryption2 = Decryption("plaintext2", "key2", -1)
    assert decryption2 < decryption1
