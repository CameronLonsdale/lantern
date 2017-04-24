"""building map of ngrams from file"""
import os


class LanguageFrequency:
    def __init__(self, ngram_files, seperator=" "):
        self.sep = seperator
        self.files = ngram_files
        self._unigrams = None
        self._bigrams = None
        self._trigrams = None
        self._quadgrams = None

    def unigrams(self):
        if self._unigrams is None:
            file = self.files['unigrams']
            self._unigrams = frequency_from_file(file, self.sep)
        return self._unigrams

    def bigrams(self):
        if self._bigrams is None:
            file = self.files['bigrams']
            self._bigrams = frequency_from_file(file, self.sep)
        return self._bigrams

    def trigrams(self):
        if self._trigrams is None:
            file = self.files['trigrams']
            self._trigrams = frequency_from_file(file, self.sep)
        return self._trigrams

    def quadgrams(self):
        if self._quadgrams is None:
            file = self.files['quadgrams']
            self._quadgrams = frequency_from_file(file, self.sep)
        return self._quadgrams


def frequency_from_file(file, sep=" "):
    ngrams = {}
    with open(file) as f:
        for line in f:
            ngram, count = line.split(sep)
            ngrams[ngram.upper()] = int(count)

    length = len(ngram)
    total = sum(ngrams.values())
    return ngrams


dir_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'english_ngrams'
)

UNIGRAM_FILE = os.path.join(dir_path, 'english_unigrams')
BIGRAM_FILE = os.path.join(dir_path, 'english_bigrams')
TRIGRAM_FILE = os.path.join(dir_path, 'english_trigrams')
QUADGRAM_FILE = os.path.join(dir_path, 'english_quadgrams')

english_ngrams_to_file = {
    'unigrams': UNIGRAM_FILE,
    'bigrams': BIGRAM_FILE,
    'trigrams': TRIGRAM_FILE,
    'quadgrams': QUADGRAM_FILE
}
english_frequency = LanguageFrequency(english_ngrams_to_file)
