"""Chi Squared Scoring function"""

from lantern.analysis import (
    frequency_analyze, chi_squared
)


class ChiSquared:
    """Score a text by comparing its frequency distribution against another."""
    def __init__(self, target_frequency_map, ngram=1):
        self.target_frequency = target_frequency_map
        self.ngram = 1

    def __call__(self, text):
        return -chi_squared(frequency_analyze(text, self.ngram), self.target_frequency)