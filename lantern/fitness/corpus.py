"""Score plaintext based on number of words identified are in the corpus."""

import string
from math import log10

from lantern.util import remove


class Corpus:
    """Scoring function based on existance of words in a corpus.

    Todo:
        This is fairly broken. I'm not happy with this implementation
        and will be changing it in the future when I revisit weighted mean scoring
    """

    def __init__(self, corpus):
        """Build function with set of words from a corpus.

        Args:
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

        Args:
            text (str): The text to score

        Returns:
            Corpus score for text
        """
        text = remove(text, string.punctuation)
        words = text.split()

        invalid_words = list(filter(lambda word: word and word.lower() not in self.words, words))
        return len(invalid_words) * self.floor
