"""Fitness scoring using ngram frequency."""
import os
from math import log10

from lantern.util import remove_punct_and_whitespace


class NgramScore():
    """Computes the score of a text by using the calculated probabilities from a loaded ngramfile."""

    def __init__(self, ngramfile, sep=' '):
        """Load file with ngrams and calculate log probailities."""
        self.ngrams = {}
        with open(ngramfile) as f:
            for line in f:
                ngram, count = line.split(sep)
                self.ngrams[ngram.upper()] = int(count)

        self.length = len(ngram)
        self.total = sum(self.ngrams.values())

        # Calculate the log probability
        self.ngrams = {
            k: log10(float(v) / self.total) for k, v in self.ngrams.items()
        }
        self.floor = log10(0.01 / self.total)

    def __call__(self, text):
        """Compute the probability of text being a valid string in the source language."""
        text = remove_punct_and_whitespace(text)
        score = 0

        for i in range(len(text) - self.length + 1):
            ngram = text[i: i + self.length]
            score += self.ngrams[ngram] if ngram in self.ngrams else self.floor

        return score


dir_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'english_ngrams'
)

QUINTGRAM_FILE = os.path.join(dir_path, 'english_quintgrams.txt')
QUAGRAM_FILE = os.path.join(dir_path, 'english_quadgrams.txt')
TRIGRAM_FILE = os.path.join(dir_path, 'english_trigrams.txt')
BIGRAM_FILE = os.path.join(dir_path, 'english_bigrams.txt')
UNIGRAM_FILE = os.path.join(dir_path, 'english_unigrams.txt')

_quintgram = None
_quadgram = None
_trigram = None
_bigram = None
_unigram = None


def quintgram():
    global _quintgram
    if _quintgram is None:
        _quintgram = NgramScore(QUINTGRAM_FILE)
    return _quintgram


def quadgram():
    global _quadgram
    if _quadgram is None:
        _quadgram = NgramScore(QUAGRAM_FILE)
    return _quadgram


def trigram():
    global _trigram
    if _trigram is None:
        _trigram = NgramScore(TRIGRAM_FILE)
    return _trigram


def bigram():
    global _bigram
    if _bigram is None:
        _bigram = NgramScore(BIGRAM_FILE)
    return _bigram


def unigram():
    global _unigram
    if _unigram is None:
        _unigram = NgramScore(UNIGRAM_FILE)
    return _unigram
