"""Fitness scoring using ngram frequency."""
import os
from math import log10

from lantern.util import remove_punct_and_whitespace

from lantern.analysis import (
    frequency_from_file, english_frequency
)


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

    @classmethod
    def from_file(cls, file, sep=' '):
        """Load file with ngrams and calculate log probailities."""
        cls(frequency_from_file(file, sep))

    def __call__(self, text):
        """Compute the probability of text being a valid string in the source language."""
        text = remove_punct_and_whitespace(text)
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

    def unigrams(self):
        if self._unigrams is None:
            self._unigrams = NgramScore(self.frequency_maps['unigrams']())
        return self._unigrams

    def bigrams(self):
        if self._bigrams is None:
            self._bigrams = NgramScore(self.frequency_maps['bigrams']())
        return self._bigrams

    def trigrams(self):
        if self._trigrams is None:
            self._trigrams = NgramScore(self.frequency_maps['trigrams']())
        return self._trigrams

    def quadgrams(self):
        if self._quadgrams is None:
            self._quadgrams = NgramScore(self.frequency_maps['quadgrams']())
        return self._quadgrams


english_ngram_to_frequency_lambda_map = {
    'unigrams': english_frequency.unigrams,
    'bigrams': english_frequency.bigrams,
    'trigrams': english_frequency.trigrams,
    'quadgrams': english_frequency.quadgrams
}

english_scorer = LanguageNGrams(english_ngram_to_frequency_lambda_map)
