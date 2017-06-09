"""Fitness scoring using ngram frequency."""

import string
from math import log10

from lantern.util import remove
from lantern.analysis import frequency


class NgramScore():
    """
    Computes the score of a text by using the frequencies of ngrams.

    Parameters:
        frequency_map (dict): ngram to frequency mapping
    """

    def __init__(self, frequency_map):
        self.ngrams = frequency_map
        self.length = len(list(self.ngrams.keys())[0])
        self.total = sum(self.ngrams.values())

        # Calculate the log probability
        self.ngrams = {
            k: log10(float(v) / self.total) for k, v in self.ngrams.items()
        }
        self.floor = log10(0.01 / self.total)

    def __call__(self, text):
        """Compute the probability of text being a valid string in the source language."""
        text = remove(text.upper(), string.whitespace + string.punctuation)
        score = 0

        for i in range(len(text) - self.length + 1):
            ngram = text[i: i + self.length]
            score += self.ngrams[ngram] if ngram in self.ngrams else self.floor

        return score


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
