"""Fitness scoring using ngram frequency."""
import os
from math import log10


class NgramScore():
    """
    NgramScorer.

    Computes the score of a text by using the calculated probabilities from a loaded ngramfile.
    """

    def __init__(self, ngramfile, sep=' '):
        """Load file with ngram counts and calucalte probailities."""
        self.ngrams = dict()
        with open(ngramfile) as f:
            for line in f:
                ngram, count = line.split(sep)
                self.ngrams[ngram.upper()] = int(count)

        self.length = len(ngram)
        self.total = sum(self.ngrams.values())

        # Calculate the log probability
        for key in self.ngrams:
            self.ngrams[key] = log10(float(self.ngrams[key]) / self.total)

        self.floor = log10(0.01 / self.total)

    def score(self, text):
        score = 0
        for i in range(len(text) - self.length + 1):
            ngram = text[i: i + self.length]
            if ngram in self.ngrams:
                score += self.ngrams[ngram]
            else:
                # Push bad solutions down
                score += self.floor
        return score


dir_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'english_ngrams'
)

QUINTGRAM_FILE = os.path.join(dir_path, 'english_quintgrams.txt')
QUAGRAM_FILE = os.path.join(dir_path, 'english_quadgrams.txt')
TRIGRAM_FILE = os.path.join(dir_path, 'english_trigrams.txt')
BIGRAM_FILE = os.path.join(dir_path, 'english_bigrams.txt')
MONOGRAM_FILE = os.path.join(dir_path, 'english_monograms.txt')

quintgram_score = NgramScore(QUINTGRAM_FILE)
quadgram_score = NgramScore(QUAGRAM_FILE)
trigram_score = NgramScore(TRIGRAM_FILE)
bigram_score = NgramScore(BIGRAM_FILE)
monogram_score = NgramScore(MONOGRAM_FILE)
