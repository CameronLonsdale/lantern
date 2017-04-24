from lantern.analysis import (
    frequency_analyze, english_unigram, chi_squared
)


class ChiSquared:
    def __init__(self, target_frequency):
        self.target_frequency = target_frequency

    def __call__(self, text):
        return -chi_squared(frequency_analyze(text), self.target_frequency)


_english_chi_squared = None


def english():
    global _english_chi_squared
    if _english_chi_squared is None:
        _english_chi_squared = ChiSquared(english_unigram())
    return _english_chi_squared
