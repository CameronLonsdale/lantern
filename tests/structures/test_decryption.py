"""Tests for the Decryption Structure"""

from lantern.structures import Decryption


def test_using_decryption():
    decryption = Decryption(plaintext="plaintext", score=0, key="key")
    assert decryption.plaintext == "plaintext"
    assert decryption.score == 0
    assert decryption.key == "key"
