"""General purpose frequency analysis tools"""

import importlib

from collections import defaultdict


# TODO: Am I handling stripping away punctuation here? Should that be default or optional?
# I think punction should be kept by default.
# If a user wants to take the frequency with all punctuation characters remove they
# can either use the keep_punct flag or strip it themselves
# TODO: work with different sized ngrams
def frequency_analyze(text, n=1):
    """
    Analyze the frequency of ngrams for a piece of text

    Example: ::

        frequency_analyze("abb") == {'a': 1, 'b': 2}

    Parameters:
        text (str): The text to analyze

    Return:
        Dictionary of symbols to frequency
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

    Parameters:
        frequency_map (dict): The dictionary to transform
        decorator (lambda): A function to manipulate the probability

    Return:
        Dictionary of symbols to probability
    """
    total = sum(frequency_map.values())
    return {k: decorator(float(v) / total) for k, v in frequency_map.items()}


def index_of_coincidence(text):
    """
    Calculate the index of coincidence for a piece of ``text``

    Example: ::

        index_of_coincidence("aabbc") == 0.2

    Parameters:
        text (str): The text to analyze

    Return:
        Decimal value of the index of coincidence
    """
    return _calculate_ioc(frequency_analyze(text), len(text))


def delta_index_of_coincidence(*texts):
    """
    Calculate the delta index of coincidence for several ``texts``

    Example: ::

        delta_index_of_coincidence("aabbc", "abbcc") == 0.2

    Parameters:
        texts (variable length arg list): The texts to analyze

    Return:
        Decimal value of the average index of coincidence
    """
    average = sum(index_of_coincidence(text) for text in texts)
    try:
        return average / len(texts)
    except ZeroDivisionError:
        raise ValueError("texts must not be empty")


# TODO: SOLVE THE KEY ERROR PROBLEM
# IF a key is not present in the target frequency then its expected value is 0??
def chi_squared(source_frequency, target_frequency):
    """
    Calculate the Chi Squared Statistic by comparing ``source_frequency`` with ``target_frequency``

    Example: ::

        chi_squared({'a': 2, 'b':3}, {'a':1, 'b':2}) == 0.1

    Parameters
        source_frequency (dict): Frequency map of the text you are analyzing
        target_frequency (dict): Frequency map of the target language to compare with

    Return:
        Decimal value of the chi-squared statistic
    """
    target_prob = frequency_to_probability(target_frequency)
    source_len = sum(source_frequency.values())
    return sum(_calculate_chi_squared(source_frequency, target_prob, source_len, n) for n in source_frequency)


ENGLISH_IC = 0.066


def _calculate_ioc(frequency_map, length):
    coms_of_letters = sum((frequency_map[symbol] * (frequency_map[symbol] - 1)) for symbol in frequency_map)
    # TODO: NOT SURE IF BEST APPROACH
    try:
        return float(coms_of_letters) / (length * (length - 1))
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
            'unigrams': (lambda: _load_ngram('unigrams'))
        })
        english.unigrams

    Parameters:
        ngrams_builders (dict): A dictionary of attribute name to attribute builder
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


def _load_ngram(name):
    module = importlib.import_module('lantern.analysis.english_ngrams.{}'.format(name))
    return getattr(module, name)

english = LanguageFrequency({
    'unigrams': (lambda: _load_ngram('unigrams')),
    'bigrams': (lambda: _load_ngram('bigrams')),
    'trigrams': (lambda: _load_ngram('trigrams')),
    'quadgrams': (lambda: _load_ngram('quadgrams'))
})
