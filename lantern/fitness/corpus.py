"""Score plaintext based on number of words identified are in the corpus"""

import string

from math import log10

from lantern.util import remove


class Corpus():
    """Scoring function based on existance of words in a corpus."""

    def __init__(self, corpus):
        """Build function with set of words from a corpus.

        Parameters:
            corpus (collection): collection of words to use
        """
        self.words = corpus
        self.floor = log10(0.01 / len(self.words))

    def __call__(self, text):
        """Score based on number of words not in the corpus.

        Example:
            >>> fitness = Corpus(["example"])
            >>> fitness("example")
            0

            >>> fitness("different")
            -2.0

        Parameters:
            text (str): The text to score

        Return:
            Corpus score for text
        """
        text = remove(text, string.punctuation)
        words = text.split()

        invalid_words = list(filter(lambda word: word and word.lower() not in self.words, words))
        return len(invalid_words) * self.floor
