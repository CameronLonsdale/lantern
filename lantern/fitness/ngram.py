"""Fitness scoring using ngram frequency."""

import string
from math import log10

from lantern.analysis import frequency
from lantern.util import remove, iterate_ngrams


class NgramScore():
    """Computes the score of a text by using the frequencies of ngrams."""

    def __init__(self, frequency_map):
        """
        Parameters:
            frequency_map (dict): ngram to frequency mapping
        """
        # Calculate the log probability
        self.length = len(list(frequency_map.keys())[0])
        self.floor = log10(0.01 / sum(frequency_map.values()))
        self.ngrams = frequency.frequency_to_probability(frequency_map, decorator=lambda f: log10(f))

    def __call__(self, text):
        """Compute the probability of text being a valid string in the source language.

        Example:
            >>> fitness = NgramScore(english.unigrams)
            >>> fitness("ABC")
            -4.3622319742618245

        Parameters:
            text (str): The text to score

        Return:
            Probability of correct decryption according to ngram frequency
        """
        text = remove(text.upper(), string.whitespace + string.punctuation)
        return sum(self.ngrams.get(ngram, self.floor) for ngram in iterate_ngrams(text, self.length))


# TODO: This can be refactored with LanguageFrequency
class LanguageNGrams:
    def __init__(self, ngram_builders):
        self.ngram_builders = ngram_builders

    def __getattr__(self, name):
        try:
            ngram_map = self.ngram_builders[name]()
        except KeyError:
            raise AttributeError("'LanguageNgrams' object has no attribute '{}'".format(name))
        else:
            setattr(self, name, ngram_map)
            return ngram_map


english = LanguageNGrams({
    'unigrams': (lambda: NgramScore(frequency.english.unigrams)),
    'bigrams': (lambda: NgramScore(frequency.english.bigrams)),
    'trigrams': (lambda: NgramScore(frequency.english.trigrams)),
    'quadgrams': (lambda: NgramScore(frequency.english.quadgrams))
})
"""English ngram scorers."""
