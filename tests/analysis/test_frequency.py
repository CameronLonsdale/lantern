"""Tests for the frequency module in analysis"""

import pytest

from lantern.analysis import frequency


def test_frequency_analyze():
    """Testing frequency analyze works for ngram = 1"""
    assert frequency.frequency_analyze("abb") == {'a': 1, 'b': 2}


def test_frequency_analyze_bigram():
    """Testing frequency analyze works for ngram = 2"""
    assert frequency.frequency_analyze("abb", 2) == {'ab': 1, 'bb': 1}


def test_frequency_analyze_empty_string():
    """Testing empty string can be frequency analyzed"""
    assert frequency.frequency_analyze("") == {}


def test_frequency_to_probability():
    """Testing frequency map is converted to probability distribution succesfully"""
    frequency_map = {'a': 1, 'b': 2}
    assert frequency.frequency_to_probability(frequency_map) == {'a': 1.0 / 3, 'b': 2.0 / 3}


def test_frequency_to_probability_empty():
    """Testing empty frequency_map is converted to empty probability distribution"""
    assert frequency.frequency_to_probability({}) == {}


def test_index_of_coincidence():
    """Testing index of coincidence for a piece of text"""
    assert frequency.index_of_coincidence("aabbc") == 0.2


def test_index_of_coincidence_multiple_texts():
    """Testing index of coincidence with multiple texts"""
    assert frequency.index_of_coincidence("aabbc", "abbcc") == 0.2


def test_index_of_coincidence_none():
    """Testing index of coincidence raises value error on empty texts"""
    with pytest.raises(ValueError):
        frequency.index_of_coincidence()


def test_index_of_coincidence_empty():
    """Testing index of coincidence for empty string raises ValueError"""
    with pytest.raises(ValueError):
        frequency.index_of_coincidence("")


def test_chi_squared():
    """Testing matching frequency distributions have chi squared of 0"""
    assert frequency.chi_squared({'a': 2, 'b': 3}, {'a': 2, 'b': 3}) == 0


def test_chi_squared_similar():
    """Testing similar frequency distributions have chi squared of 0.1"""
    assert frequency.chi_squared({'a': 2, 'b': 3}, {'a': 1, 'b': 2}) == 0.1


def test_chi_squared_different_symbols():
    """Testing different symbols are handled appropriately"""
    assert frequency.chi_squared({'a': 1, 'd': 3}, {'a': 1}) == 0


def test_languagefrequency_attribute_access():
    """Testing correct attributes are found, incorrect attributes raise AttributeErrors"""
    frequency.english.unigrams

    with pytest.raises(AttributeError):
        frequency.english.invalid
