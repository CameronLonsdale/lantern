"""Testing NgramScore fitness function"""

from lantern.fitness import NgramScorer


def test_ngram_score():
    """Testing NgramScore"""
    scorer = NgramScorer({'a': 1, 'b': 1})
    assert round(scorer("abb")) == -7
