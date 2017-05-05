"""Fitness scoring using ngram frequency."""
import os
import string
from math import log10

from lantern.util import remove

from lantern.analysis import frequency


class NgramScore():
    """Computes the score of a text by using the frequencies of ngrams."""
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
        text = text.upper()
        text = remove(text, string.whitespace + string.punctuation)
        score = 0

        for i in range(len(text) - self.length + 1):
            ngram = text[i: i + self.length]
            score += self.ngrams[ngram] if ngram in self.ngrams else self.floor

        return score


class LanguageNGrams:
    def __init__(self, frequency_maps):
        self.frequency_maps = frequency_maps
        self._unigrams = None
        self._bigrams = None
        self._trigrams = None
        self._quadgrams = None

    @property
    def unigrams(self):
        if self._unigrams is None:
            self._unigrams = NgramScore(self.frequency_maps['unigrams']())
        return self._unigrams

    @property
    def bigrams(self):
        if self._bigrams is None:
            self._bigrams = NgramScore(self.frequency_maps['bigrams']())
        return self._bigrams

    @property
    def trigrams(self):
        if self._trigrams is None:
            self._trigrams = NgramScore(self.frequency_maps['trigrams']())
        return self._trigrams

    @property
    def quadgrams(self):
        if self._quadgrams is None:
            self._quadgrams = NgramScore(self.frequency_maps['quadgrams']())
        return self._quadgrams


english_ngram_to_frequency_lambda_map = {
    'unigrams': lambda: frequency.english.unigrams,
    'bigrams': lambda: frequency.english.bigrams,
    'trigrams': lambda: frequency.english.trigrams,
    'quadgrams': lambda: frequency.english.quadgrams
}

english = LanguageNGrams(english_ngram_to_frequency_lambda_map)
