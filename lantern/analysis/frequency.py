"""General purpose frequency analysis tools"""

import importlib

from collections import defaultdict


# TODO: Am I handling stripping away punctuation here? Should that be default or optional?
# I think punction should be kept by default.
# If a user wants to take the frequency with all punctuation characters remove they can either use the keep_punct flag or strip it themselves
# TODO: work with different sized ngrams
def frequency_analyze(text, n=1):
    """
    Analyze the frequency of ngrams for a piece of text

    Example: ::

        frequency_analyze("abb") == {'a': 1, 'b': 2}

    :param str text: The text to analyze
    :return: Dictionary of symbols to frequency
    """
    frequency = defaultdict(lambda: 0, {})
    for symbol in text:
        frequency[symbol] += 1

    return frequency


def frequency_to_probability(frequency_map, decorator=lambda f: f):
    """
    Transform a ``frequency_map`` into a map of probability

    Example: ::

        frequency_to_probability({'a': 1, 'b': 2}) == {'a': 1/3, 'b': 2/3}

    :param dict frequency_map: The dictionary to transform
    :param lambda decorator: A function to manipulate the probability
    :return: Dictionary of symbols to probability
    """
    total = sum(frequency_map.values())
    return {k: decorator(float(v) / total) for k, v in frequency_map.items()}


def index_of_coincidence(text):
    """
    Calculate the index of coincidence for a piece of ``text``

    Example: ::

        index_of_coincidence("aabbc") == 0.2

    :param str text: The text to analyze
    :return: Decimal value of the index of coincidence
    """
    frequency = frequency_analyze(text)
    N = len(text)
    return _calculate_ioc(frequency, N)


def delta_index_of_coincidence(texts):
    """
    Calculate the delta index of coincidence for several ``texts``

    Example: ::

        delta_index_of_coincidence(["aabbc", "abbcc"]) == 0.2

    :param iterable texts: The texts to analyze
    :return: Decimal value of the average index of coincidence
    """
    average = 0
    for text in texts:
        average += index_of_coincidence(text)

    # TODO: Not sure if best approach
    try:
        return average / len(texts)
    except ZeroDivisionError:
        return 0


# TODO: SOLVE THE KEY ERROR PROBLEM
# IF a key is not present in the target frequency then its expected value is 0??
def chi_squared(source_frequency, target_frequency):
    """
    Calculate the Chi Squared Statistic by comparing ``source_frequency`` with ``target_frequency``

    Example: ::

        chi_squared({'a': 2, 'b':3}, {'a':1, 'b':2}) == 0.1

    :param dict source_frequency: Frequency map of the text you are analyzing
    :param dict target_frequency: Frequency map of target language to compare with
    :return: Decimal value of the Chi Squared Statistic
    """
    target_prob = frequency_to_probability(target_frequency)
    source_len = sum(source_frequency.values())
    return sum(_calculate_chi_squared(source_frequency, target_prob, source_len, n) for n in source_frequency)


ENGLISH_IC = 0.066


def _calculate_ioc(frequency_map, N):
    coms_of_letters = sum((frequency_map[n] * (frequency_map[n] - 1)) for n in frequency_map)
    # TODO: NOT SURE IF BEST APPROACH
    try:
        return float(coms_of_letters) / (N * (N - 1))
    except ZeroDivisionError:
        return 0


def _calculate_chi_squared(source_frequency, target_prob, source_len, n):
    # TODO: Fairly sure this is wrong
    if n not in target_prob:
        return 0

    return (source_frequency[n] - source_len * target_prob[n])**2 / (source_len * target_prob[n])


class LanguageFrequency:
    """
    A LanguageFrequency object, to hold frequency distributions for a language.
    On Attribute access, if the ngram does not exist, it is built using a given builder.
    Any subsequent accesses then use the existing frequney map

    Example: ::

        english = LanguageFrequency({
            'unigrams': (lambda: _load_ngram('unigrams')),
            'bigrams': (lambda: _load_ngram('bigrams')),
            'trigrams': (lambda: _load_ngram('trigrams')),
            'quadgrams': (lambda: _load_ngram('quadgrams'))
        })

    :param dict ngram_builders: A dictionary of attribute name to attribute builder
    """

    def __init__(self, ngram_builders):
        self.ngram_builders = ngram_builders

    def __getattr__(self, name):
        try:
            ngram_map = self.ngram_builders[name]()
        except KeyError:
            raise AttributeError("'LanguageFrequency' object has no attribute '{}'".format(name))
        else:
            setattr(self, name, ngram_map)
            return ngram_map


# FUNCTION IS CURRENTLY UNUSED. NOT SURE IF WORTH KEEPING OR NOT.
# def frequency_from_file(file, sep=" "):
#     ngrams = {}
#     with open(file) as f:
#         for line in f:
#             ngram, count = line.split(sep)
#             ngrams[ngram.upper()] = int(count)

#     length = len(ngram)
#     total = sum(ngrams.values())
#     return ngrams


def _load_ngram(name):
    module = importlib.import_module('lantern.analysis.english_ngrams.{}'.format(name))
    return getattr(module, name)

english = LanguageFrequency({
    'unigrams': (lambda: _load_ngram('unigrams')),
    'bigrams': (lambda: _load_ngram('bigrams')),
    'trigrams': (lambda: _load_ngram('trigrams')),
    'quadgrams': (lambda: _load_ngram('quadgrams'))
})
