"""Testing NgramScore fitness function"""

from lantern.fitness import NgramScore


def test_ngram_score():
    """Testing NgramScore"""
    scorer = NgramScore({'a': 1, 'b': 1})
    assert round(scorer("abb")) == -7
