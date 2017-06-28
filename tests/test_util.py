"""Test utility functions"""

import pytest

import string

from lantern.util import (
    remove, split_columns, combine_columns,
    iterate_ngrams, group
)


def test_remove_with_punctuation():
    """Testing punctuation is removed"""
    assert remove("Don't worry my friends.", string.punctuation) == "Dont worry my friends"


def test_remove_with_whitespace():
    """Testing whitespace is removed"""
    assert remove("Don't worry my friends.", string.whitespace) == "Don'tworrymyfriends."


def test_remove_with_list_and_set():
    """Testing remove with exclude as a set or list"""
    assert remove("example", ['e', 'x']) == "ampl"
    assert remove("example", set(['e', 'x'])) == "ampl"


def test_columns_length_1():
    """Testing splitting and combining 1 column text works"""
    text = "example"
    split = split_columns(text, 1)

    assert split == [text]
    assert combine_columns(split) == text


def test_columns_lower_length():
    """Testing split and combine columns where n_columns is less than the length of text"""
    text = "example"
    split = split_columns(text, 4)

    assert split == ['ep', 'xl', 'ae', 'm']
    assert combine_columns(split) == text


def test_columns_same_length():
    """Testing split and combine where n_columns = len(text)"""
    text = "example"
    split = split_columns(text, len(text))

    assert split == list(text)
    assert combine_columns(split) == text


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


def test_iterate_ngrams():
    """Testing iterating ngrams works"""
    assert list(iterate_ngrams("example", 4)) == ['exam', 'xamp', 'ampl', 'mple']


def test_iterate_ngrams_empty():
    """Testing empty string returns no ngrams"""
    assert list(iterate_ngrams("", 1)) == []


def test_iterate_ngrams_non_positive():
    """Testing non positive n values raise ValueError"""
    with pytest.raises(ValueError):
        list(iterate_ngrams("example", 0))

    with pytest.raises(ValueError):
        list(iterate_ngrams("example", -1))


def test_group_even_length():
    """Testing group with even length string"""
    assert group("test", 2) == ['te', 'st']


def test_group_odd_length():
    """Testing group with odd length string"""
    assert group("example", 2) == ['ex', 'am', 'pl', 'e']


def test_group_invalid():
    """Testing non positive sizes raise ValueError"""
    with pytest.raises(ValueError):
        list(group("example", 0))

    with pytest.raises(ValueError):
        list(group("example", -1))
