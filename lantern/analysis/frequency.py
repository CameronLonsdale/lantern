import importlib

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
    if n not in target_prob:
        return 0

    return (source_frequency[n] - source_len * target_prob[n])**2 / (source_len * target_prob[n])


class LanguageFrequency:
    def __init__(self, ngram_builders):
        self.ngram_builders = ngram_builders
        self._unigrams = None
        self._bigrams = None
        self._trigrams = None
        self._quadgrams = None

    @property
    def unigrams(self):
        if self._unigrams is None:
            self._unigrams = self.ngram_builders['unigrams']()
        return self._unigrams

    @property
    def bigrams(self):
        if self._bigrams is None:
            self._bigrams = self.ngram_builders['bigrams']()
        return self._bigrams

    @property
    def trigrams(self):
        if self._trigrams is None:
            self._trigrams = self.ngram_builders['trigrams']()
        return self._trigrams

    @property
    def quadgrams(self):
        if self._quadgrams is None:
            self._quadgrams = self.ngram_builders['quadgrams']()
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


def _load_ngram(name):
    module = importlib.import_module('lantern.analysis.english_ngrams.{}'.format(name))
    return getattr(module, name)

ngram_builders = {
    'unigrams': (lambda: _load_ngram('unigrams')),
    'bigrams': (lambda: _load_ngram('bigrams')),
    'trigrams': (lambda: _load_ngram('trigrams')),
    'quadgrams': (lambda: _load_ngram('quadgrams'))
}
english = LanguageFrequency(ngram_builders)
