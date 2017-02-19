"""Score plaintext based on number of words identified are in the ."""
import nltk.corpus
from math import log10

from cckrypto.util import (
    remove_punctuation, remove_punct_and_whitespace
)


class Corpus():
    """Scoring function based on existance of words in a corpus."""

    def __init__(self, corpus):
        """Build function with set of words from a corpus."""
        self.words = corpus
        self.floor = log10(0.01 / len(self.words))

    def score(self, text, whitespace_hint):
        """Score based on number of words no in the corpus."""
        if whitespace_hint:
            text = remove_punctuation(text)
            text_words = text.split()
        else:
            text = remove_punct_and_whitespace(text)
            raise NotImplemented()

        n_incorrect_words = 0
        for word in text_words:
            if word and word.lower() not in self.words:
                # print(word + ' in words? ' + str(word in WORDS))
                n_incorrect_words += 1

        if n_incorrect_words == 0:
            return 0

        return n_incorrect_words * self.floor

english_words = Corpus(nltk.corpus.words.words())
