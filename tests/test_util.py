"""Test utility functions"""

import pytest

import string

from lantern.util import (
    remove, split_columns, combine_columns
)


def test_remove_with_punctuation():
    """Test punctuation removed"""
    plaintext = "Don't worry my friends."
    assert remove(plaintext, string.punctuation) == "Dont worry my friends"


def test_remove_with_whitespace():
    """Test whitespace removed"""
    plaintext = "Don't worry my friends."
    assert remove(plaintext, string.whitespace) == "Don'tworrymyfriends."


def test_remove_with_list_and_set():
    """Test remove with list and set excludes"""
    plaintext = "example"
    assert remove(plaintext, ['e', 'x']) == "ampl"
    assert remove(plaintext, set(['e', 'x'])) == "ampl"


def test_columns_length_1():
    """Since splitting into 1 column works, you should be able to combine 1 columns"""
    text = "example"
    split = split_columns(text, 1)

    assert split == [text]
    assert combine_columns(*split) == text


def test_columns_lower_length():
    """Testing split and combine columns where num columns is less than the length of text"""
    text = "example"
    split = split_columns(text, 4)

    assert split == ['ep', 'xl', 'ae', 'm']
    assert combine_columns(*split) == text


def test_columns_same_length():
    """Testing split and combine where n_cols = len(text)"""
    text = "example"
    split = split_columns(text, len(text))

    assert split == list(text)
    assert combine_columns(*split) == text


def test_split_columns_invalid_values():
    """Testing split columns with invalid lengths raise ValueError"""
    with pytest.raises(ValueError):
        split_columns("example", -1)

    with pytest.raises(ValueError):
        split_columns("example", -200)

    with pytest.raises(ValueError):
        split_columns("example", 0)

    with pytest.raises(ValueError):
        split_columns("example", 200)


def test_combine_columns_invalid_values():
    """Testing combine columns with no columns raises ValueError"""
    with pytest.raises(ValueError):
        combine_columns()
