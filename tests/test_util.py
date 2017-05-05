"""Test utility functions"""

import string

from lantern.util import (
    remove, split_columns, combine_columns
)


def test_remove_with_punctuation():
    """Test punctuation removed"""
    plaintext = "Don't worry my friends."
    assert remove(
        plaintext, string.punctuation
    ) == "Dont worry my friends"


def test_remove_with_whitespace():
    """Test whitespace removed"""
    plaintext = "Don't worry my friends."
    assert remove(
        plaintext, string.whitespace
    ) == "Don'tworrymyfriends."
