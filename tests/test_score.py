"""Test the scoring algorithm"""

from lantern import score


def test_score_with_single_function():
    """Single function accepted instead of iterable"""
    plaintext = "lorem ipsum"
    assert score(plaintext, lambda _: 15) == 15


def test_score_is_averaged_positive():
    """Score is averaged over number of functions used"""
    plaintext = "lorem ipsum"
    assert score(
        plaintext,
        scoring_functions=[lambda _: 10, lambda _: 20]
    ) == 15


def test_score_is_averaged_negative():
    """Score is averaged over number of functions used"""
    plaintext = "lorem ipsum"
    assert score(
        plaintext,
        scoring_functions=[lambda _: -10, lambda _: -20]
    ) == -15


def test_score_is_averaged_positive_and_negative():
    """Score is averaged over number of functions used"""
    plaintext = "lorem ipsum"
    assert score(
        plaintext,
        scoring_functions=[lambda _: -10, lambda _: 2]
    ) == -4
