"""General purpose frequency analysis tools."""

import importlib
from collections import Counter

from lantern.util import iterate_ngrams


def frequency_analyze(text, n=1):
    """Analyze the frequency of ngrams for a piece of text.

    Examples:
        >>> frequency_analyze("abb")
        {'a': 1, 'b': 2}

        >>> frequency_analyze("abb", 2)
        {'ab': 1, 'bb': 1}

    Parameters:
        text (str): The text to analyze
        n (int): The ngram size to use

    Return:
        Dictionary of ngrams to frequency
    """
    return Counter(iterate_ngrams(text, n))


def frequency_to_probability(frequency_map, decorator=lambda f: f):
    """Transform a ``frequency_map`` into a map of probability.
    Using the sum of all frequencies as the total.

    Example:
        >>> frequency_to_probability({'a': 1, 'b': 2})
        {'a': 1/3, 'b': 2/3}

    Parameters:
        frequency_map (dict): The dictionary to transform
        decorator (function): A function to manipulate the probability

    Return:
        Dictionary of ngrams to probability
    """
    total = sum(frequency_map.values())
    return {k: decorator(float(v) / total) for k, v in frequency_map.items()}


def index_of_coincidence(*texts):
    """Calculate the index of coincidence for one or more ``texts``.
    The results are averaged over multiple texts to return the delta index of coincidence.

    Examples:
        >>> index_of_coincidence("aabbc")
        0.2

        >>> index_of_coincidence("aabbc", "abbcc")
        0.2

    Parameters:
        texts (variable length arg list): The texts to analyze

    Return:
        Decimal value of the index of coincidence

    Raises:
        ValueError: If texts is empty
        ValueError: If any text is less that 2 character long
    """
    if not texts:
        raise ValueError("texts must not be empty")

    total = sum(_calculate_index_of_coincidence(frequency_analyze(text), len(text)) for text in texts)
    return total / len(texts)


def chi_squared(source_frequency, target_frequency):
    """Calculate the Chi Squared statistic by comparing ``source_frequency`` with ``target_frequency``.

    Example:
        >>> chi_squared({'a': 2, 'b': 3}, {'a': 1, 'b': 2})
        0.1

    Parameters:
        source_frequency (dict): Frequency map of the text you are analyzing
        target_frequency (dict): Frequency map of the target language to compare with

    Return:
        Decimal value of the chi-squared statistic
    """
    target_prob = frequency_to_probability(target_frequency)
    # Ignore any symbols from source that are not in target.
    # TODO: raise Error if source_len is 0?
    source_len = sum(v for k, v in source_frequency.items() if k in target_frequency)
    return sum(_calculate_chi_squared(source_frequency.get(symbol, 0), prob, source_len) for symbol, prob in target_prob.items())


def _calculate_index_of_coincidence(frequency_map, length):
    """A measure of how similar frequency_map is to the uniform distribution.
    Or the probability that two letters picked randomly are alike.
    """
    if length <= 1:
        raise ValueError("length must be greater than 1")  # Could change this to 0 or Nan. Future decision.

    # Mathemtical combination, number of ways to choose 2 letters, no replacement, order doesnt matter
    combination_of_letters = sum((frequency_map[symbol] * (frequency_map[symbol] - 1)) for symbol in frequency_map)
    return float(combination_of_letters) / (length * (length - 1))


def _calculate_chi_squared(source_freq, target_prob, source_len):
    """A measure of the observed frequency of the symbol versus the expected frequency.
    If the value is 0 then the texts are exactly alike for that symbol.
    """
    expected = source_len * target_prob
    return (source_freq - expected)**2 / expected


class LanguageFrequency:
    """A LanguageFrequency object to hold frequency distributions for a language.
    On Attribute access if the ngram does not exist it is built using a given builder.
    Any subsequent accesses then use the existing ngram map

    Example:
        >>> english = LanguageFrequency({'unigrams': lambda: _load_ngram('unigrams')})
        >>> english.unigrams
        {'A': 374061888, 'B': 70195826, ...}
    """

    def __init__(self, ngram_builders):
        """
        Parameters:
            ngrams_builders (dict): A dictionary of attribute name to attribute builder
        """
        self.ngram_builders = ngram_builders

    def __getattr__(self, name):
        """Build attribute and set for future use.

        Parameters:
            name (str): The name of the attribute

        Raises:
            AttributeError: If the attribute cannot be built

        Return:
            The built attribute
        """
        try:
            ngram_map = self.ngram_builders[name]()
        except KeyError:
            raise AttributeError("'LanguageFrequency' object has no attribute '{}'".format(name))
        else:
            setattr(self, name, ngram_map)
            return ngram_map


def _load_ngram(name):
    """Dynamically import the python module with the ngram defined as a dictionary.
    Since bigger ngrams are large files its wasteful to always statically import them if they're not used.
    """
    module = importlib.import_module('lantern.analysis.english_ngrams.{}'.format(name))
    return getattr(module, name)


english = LanguageFrequency({
    'unigrams': lambda: _load_ngram('unigrams'),
    'bigrams': lambda: _load_ngram('bigrams'),
    'trigrams': lambda: _load_ngram('trigrams'),
    'quadgrams': lambda: _load_ngram('quadgrams')
})
"""English ngram frequencies."""


ENGLISH_IC = _calculate_index_of_coincidence(english.unigrams, sum(english.unigrams.values()))
"""Index of coincidence for the English language."""
