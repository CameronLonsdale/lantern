"""Test the chi-squared scoring function"""

from lantern.fitness import ChiSquared


def test_chisquared():
    """Testing chisquared fitness function"""
    scorer = ChiSquared({'a': 1, 'b': 2})
    assert scorer("aabbb") == -0.1
