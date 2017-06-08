"""Chi Squared Scoring function"""

from lantern.analysis.frequency import (
    frequency_analyze, chi_squared
)


class ChiSquared:
    """
    Score a text by comparing its frequency distribution against another.

    Parameters:
        target_frequency_map (dict): symbol to frequency mapping of the distribution you want to compare to
    """

    def __init__(self, target_frequency_map):
        self.target_frequency = target_frequency_map

    def __call__(self, text):
        return -chi_squared(frequency_analyze(text), self.target_frequency)
