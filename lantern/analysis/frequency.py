import os

from collections import defaultdict


# TODO: Am I handling stripping away punctuation here? Should that be default or optional?
# I think punction should be kept by default.
# If a user wants to take the frequency with all punctuation characters remove they can either use the keep_punct flag or strip it themselves
# TODO: work with different sized ngrams
def frequency_analyze(text, n=1, keep_punct=True):
    """
    Analyze the frequency of ngrams for a piece of text

    :param str text: the text to analyze
    :rtype: dictionary of symbols to frequency
    """
    frequency = defaultdict(lambda: 0, {})
    for symbol in text:
        frequency[symbol] += 1

    return frequency


def frequency_to_probability(frequency_map, decorator=lambda f: f):
    total = sum(frequency_map.values())
    return {k: decorator(float(v) / total) for k, v in frequency_map.items()}


def index_of_coincidence(text):
    frequency = frequency_analyze(text)
    N = len(text)
    return _calculate_ioc(frequency, N)


def avg_index_of_coincidence(texts):
    average = 0
    for text in texts:
        average += index_of_coincidence(text)
    return average / len(texts)


# TODO: SOLVE THE KEY ERROR PROBLEM
# IF a key is not present in the target frequency then its expected value is 0
def chi_squared(source_frequency, target_frequency):
    target_prob = frequency_to_probability(target_frequency)
    source_len = sum(source_frequency.values())
    return sum(_calculate_chi_squared(source_frequency, target_prob, source_len, n) for n in source_frequency)


ENGLISH_IC = 0.066


def _calculate_ioc(frequency_map, N):
    coms_of_letters = sum((frequency_map[n] * (frequency_map[n] - 1)) for n in frequency_map)
    return float(coms_of_letters) / (N * (N - 1))


def _calculate_chi_squared(source_frequency, target_prob, source_len, n):
    return (source_frequency[n] - source_len * target_prob[n])**2 / (source_len * target_prob[n])


class LanguageFrequency:
    def __init__(self, ngram_files, seperator=" "):
        self.sep = seperator
        self.files = ngram_files
        self._unigrams = None
        self._bigrams = None
        self._trigrams = None
        self._quadgrams = None

    @property
    def unigrams(self):
        if self._unigrams is None:
            file = self.files['unigrams']
            self._unigrams = frequency_from_file(file, self.sep)
        return self._unigrams

    @property
    def bigrams(self):
        if self._bigrams is None:
            file = self.files['bigrams']
            self._bigrams = frequency_from_file(file, self.sep)
        return self._bigrams

    @property
    def trigrams(self):
        if self._trigrams is None:
            file = self.files['trigrams']
            self._trigrams = frequency_from_file(file, self.sep)
        return self._trigrams

    @property
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
english = LanguageFrequency(english_ngrams_to_file)
