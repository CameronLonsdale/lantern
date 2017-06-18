"""Tests for the frequency module in analysis"""

import pytest

from lantern.analysis import frequency


def test_frequency_analyze():
    """Test frequency analyze works for ngram = 1"""
    assert frequency.frequency_analyze("abb") == {'a': 1, 'b': 2}


def test_frequency_analyze_bigram():
    """Test frequency analyze works for ngram = 2"""
    assert frequency.frequency_analyze("abb", 2) == {'ab': 1, 'bb': 1}


def test_frequency_analyze_empty_string():
    """Test empty string can be frequency analyzed"""
    assert frequency.frequency_analyze("") == {}


def test_frequency_to_probability():
    """Test frequency map is converted to probability distribution succesfully"""
    frequency_map = {'a': 1, 'b': 2}
    assert frequency.frequency_to_probability(frequency_map) == {'a': 1.0 / 3, 'b': 2.0 / 3}


def test_frequency_to_probability_empty():
    """Test empty frequency_map is converted to empty probability distribution"""
    assert frequency.frequency_to_probability({}) == {}


def test_index_of_coincidence():
    """Test index of coincidence for a piece of text"""
    assert frequency.index_of_coincidence("aabbc") == 0.2


def test_index_of_coincidence_empty():
    """Test index of coincidence for empty string"""
    assert frequency.index_of_coincidence("") == 0


def test_delta_index_of_coincidence():
    """Test delta index of coincidence for texts"""
    assert frequency.delta_index_of_coincidence("aabbc", "abbcc") == 0.2


def test_delta_index_of_coincidence_empty():
    """Test delta index of coincidence for texts"""
    with pytest.raises(ValueError):
        frequency.delta_index_of_coincidence()


def test_chi_squared():
    """Test matching frequency distributions have chi squared of 0"""
    assert frequency.chi_squared({'a': 2, 'b': 3}, {'a': 1, 'b': 2}) == 0.1


# def test_chi_squared_different_symbols():
#     """Test matching frequency distributions have chi squared of 0"""
#     assert frequency.chi_squared({'c': 1, 'd':2}, {'a':1, 'b':2}) == 0


def test_languagefrequency_attribute_access():
    """Correct attributes are found, incorrect attributes raise AttributeErrors"""
    frequency.english.unigrams

    with pytest.raises(AttributeError):
        frequency.english.invalid
