"""Tests for the Decryption Structure"""

from lantern.structures import Decryption


def test_kwargs():
    decryption = Decryption(plaintext="plaintext", score=0, key="key")
    assert decryption.plaintext == "plaintext"
    assert decryption.score == 0
    assert decryption.key == "key"


def test_args():
    decryption = Decryption("plaintext", "key", 0)
    assert decryption.plaintext == "plaintext"
    assert decryption.key == "key"
    assert decryption.score == 0
