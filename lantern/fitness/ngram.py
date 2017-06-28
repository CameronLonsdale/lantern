"""Fitness scoring using ngram frequency."""

import string
import math

from lantern.analysis import frequency
from lantern.util import remove, iterate_ngrams


def NgramScorer(frequency_map):
    """Computes the score of a text by using the frequencies of ngrams.

    Example:
        >>> fitness = NgramScore(english.unigrams)
        >>> fitness("ABC")
        -4.3622319742618245

    Args:
        frequency_map (dict): ngram to frequency mapping
    """

    # Calculate the log probability
    length = len(next(iter(frequency_map)))
    # TODO: 0.01 is a magic number. Needs to be better than that.
    floor = math.log10(0.01 / sum(frequency_map.values()))
    ngrams = frequency.frequency_to_probability(frequency_map, decorator=math.log10)

    def inner(text):
        text = remove(text.upper(), string.whitespace + string.punctuation)
        return sum(ngrams.get(ngram, floor) for ngram in iterate_ngrams(text, length))

    return inner


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
    'unigrams': (lambda: NgramScorer(frequency.english.unigrams)),
    'bigrams': (lambda: NgramScorer(frequency.english.bigrams)),
    'trigrams': (lambda: NgramScorer(frequency.english.trigrams)),
    'quadgrams': (lambda: NgramScorer(frequency.english.quadgrams))
})
"""English ngram scorers."""
