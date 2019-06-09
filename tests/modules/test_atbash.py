"""Tests for the Caeser module"""

from lantern.modules import atbash


def test_decrypt():
    """Test decryption"""
    assert atbash.decrypt("uozt{Yzybolm}") == "flag{Babylon}"


def test_encrypt():
    """Test encryption"""
    assert ''.join(atbash.encrypt("flag{Babylon}")) == "uozt{Yzybolm}"
