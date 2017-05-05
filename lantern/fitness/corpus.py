"""Score plaintext based on number of words identified are in the corpus"""
from math import log10

import string

from lantern.util import remove


class Corpus():
    """Scoring function based on existance of words in a corpus."""

    def __init__(self, corpus):
        """Build function with set of words from a corpus."""
        self.words = corpus
        self.floor = log10(0.01 / len(self.words))

    def __call__(self, text, whitespace_hint):
        """Score based on number of words not in the corpus."""
        if whitespace_hint:
            text = remove(text, string.punctuation)
            words = text.split()
        else:
            text = remove(text, string.punctuation + string.whitespace)
            raise NotImplementedError()

        invalid_words = list(filter(lambda word: word and word.lower() not in self.words, words))
        return len(invalid_words) * self.floor
