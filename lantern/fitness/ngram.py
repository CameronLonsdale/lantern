"""Fitness scoring using ngram frequency."""

import math
import string

from lantern.analysis import frequency
from lantern.structures import DynamicDict
from lantern.util import remove, iterate_ngrams


def NgramScorer(frequency_map):
    """Compute the score of a text by using the frequencies of ngrams.

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
        # I dont like this, it is only for the .upper() to work,
        # But I feel as though this can be removed in later refactoring
        text = ''.join(text)
        text = remove(text.upper(), string.whitespace + string.punctuation)
        return sum(ngrams.get(ngram, floor) for ngram in iterate_ngrams(text, length))

    return inner


english = DynamicDict({
    'unigrams': lambda: NgramScorer(frequency.english.unigrams),
    'bigrams': lambda: NgramScorer(frequency.english.bigrams),
    'trigrams': lambda: NgramScorer(frequency.english.trigrams),
    'quadgrams': lambda: NgramScorer(frequency.english.quadgrams)
})
"""English ngram scorers."""
