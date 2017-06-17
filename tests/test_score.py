"""Test the scoring algorithm"""

import pytest

from lantern import score


def test_score_with_single_function():
    """Single function accepted instead of iterable"""
    assert score("example", lambda _: 15) == 15


def test_score_is_averaged_positive():
    """Score is averaged over number of functions used"""
    assert score("example", lambda _: 10, lambda _: 20) == 15


def test_score_is_averaged_negative():
    """Score is averaged over number of functions used"""
    assert score("example", lambda _: -10, lambda _: -20) == -15


def test_score_is_averaged_positive_and_negative():
    """Score is averaged over number of functions used"""
    assert score("example", lambda _: -10, lambda _: 2) == -4


def test_score_invalid():
    """Score raises ValueError when given no scoring functions"""
    with pytest.raises(ValueError):
        score("example")
