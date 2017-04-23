"""Test utility functions"""

from lantern.util import (
    remove_punctuation, remove_whitespace,
    remove_punct_and_whitespace
)


def test_remove_punctuation():
    """Test punctuation removed"""
    plaintext = "Don't worry my friends."
    assert remove_punctuation(
        plaintext
    ) == "Dont worry my friends"


def test_remove_whitespace():
    """Test whitespace removed"""
    plaintext = "Don't worry my friends."
    assert remove_whitespace(
        plaintext
    ) == "Don'tworrymyfriends."


def test_remove_punct_and_whitespace():
    """Test punctuation and whitespace removal"""
    plaintext = "Don't worry my friends."
    assert remove_punct_and_whitespace(
        plaintext
    ) == "Dontworrymyfriends"
