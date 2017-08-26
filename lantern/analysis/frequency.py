"""General purpose frequency analysis tools."""

import importlib
import statistics
from collections import Counter

from lantern.structures import DynamicDict
from lantern.util import iterate_ngrams


def frequency_analyze(text, n=1):
    """Analyze the frequency of ngrams for a piece of text.

    Examples:
        >>> frequency_analyze("abb")
        {'a': 1, 'b': 2}

        >>> frequency_analyze("abb", 2)
        {'ab': 1, 'bb': 1}

    Args:
        text (str): The text to analyze
        n (int): The ngram size to use

    Returns:
        Dictionary of ngrams to frequency

    Raises:
        ValueError: If n is not a positive integer
    """
    return Counter(iterate_ngrams(text, n))


def frequency_to_probability(frequency_map, decorator=lambda f: f):
    """Transform a ``frequency_map`` into a map of probability using the sum of all frequencies as the total.

    Example:
        >>> frequency_to_probability({'a': 2, 'b': 2})
        {'a': 0.5, 'b': 0.5}

    Args:
        frequency_map (dict): The dictionary to transform
        decorator (function): A function to manipulate the probability

    Returns:
        Dictionary of ngrams to probability
    """
    total = sum(frequency_map.values())
    return {k: decorator(v / total) for k, v in frequency_map.items()}


def index_of_coincidence(*texts):
    """Calculate the index of coincidence for one or more ``texts``.
    The results are averaged over multiple texts to return the delta index of coincidence.

    Examples:
        >>> index_of_coincidence("aabbc")
        0.2

        >>> index_of_coincidence("aabbc", "abbcc")
        0.2

    Args:
        *texts (variable length argument list): The texts to analyze

    Returns:
        Decimal value of the index of coincidence

    Raises:
        ValueError: If texts is empty
        ValueError: If any text is less that 2 character long
    """
    if not texts:
        raise ValueError("texts must not be empty")

    return statistics.mean(_calculate_index_of_coincidence(frequency_analyze(text), len(text)) for text in texts)


def _calculate_index_of_coincidence(frequency_map, length):
    """A measure of how similar frequency_map is to the uniform distribution.
    Or the probability that two letters picked randomly are alike.
    """
    if length <= 1:
        return 0
        # We cannot error here as length can legitimiately be 1.
        # Imagine a ciphertext of length 3 and a key of length 2.
        # Spliting this text up and calculating the index of coincidence results in ['AC', 'B']
        # IOC of B will be calcuated for the 2nd column of the key. We could represent the same
        # encryption with a key of length 3 but then we encounter the same problem. This is also
        # legitimiate encryption scheme we cannot ignore. Hence we have to deal with this fact here
        # A value of 0 will impact the overall mean, however it does make some sense when you ask the question
        # How many ways to choose 2 letters from the text, if theres only 1 letter then the answer is 0.

    # Mathemtical combination, number of ways to choose 2 letters, no replacement, order doesnt matter
    combination_of_letters = sum(freq * (freq - 1) for freq in frequency_map.values())
    return combination_of_letters / (length * (length - 1))


def chi_squared(source_frequency, target_frequency):
    """Calculate the Chi Squared statistic by comparing ``source_frequency`` with ``target_frequency``.

    Example:
        >>> chi_squared({'a': 2, 'b': 3}, {'a': 1, 'b': 2})
        0.1

    Args:
        source_frequency (dict): Frequency map of the text you are analyzing
        target_frequency (dict): Frequency map of the target language to compare with

    Returns:
        Decimal value of the chi-squared statistic
    """
    # Ignore any symbols from source that are not in target.
    # TODO: raise Error if source_len is 0?
    target_prob = frequency_to_probability(target_frequency)
    source_len = sum(v for k, v in source_frequency.items() if k in target_frequency)

    result = 0
    for symbol, prob in target_prob.items():
        symbol_frequency = source_frequency.get(symbol, 0)  # Frequecy is 0 if it doesnt appear in source
        result += _calculate_chi_squared(symbol_frequency, prob, source_len)

    return result


def _calculate_chi_squared(source_freq, target_prob, source_len):
    """A measure of the observed frequency of the symbol versus the expected frequency.
    If the value is 0 then the texts are exactly alike for that symbol.
    """
    expected = source_len * target_prob
    return (source_freq - expected)**2 / expected


def _load_ngram(name):
    """Dynamically import the python module with the ngram defined as a dictionary.
    Since bigger ngrams are large files its wasteful to always statically import them if they're not used.
    """
    module = importlib.import_module('lantern.analysis.english_ngrams.{}'.format(name))
    return getattr(module, name)


english = DynamicDict({
    'unigrams': lambda: _load_ngram('unigrams'),
    'bigrams': lambda: _load_ngram('bigrams'),
    'trigrams': lambda: _load_ngram('trigrams'),
    'quadgrams': lambda: _load_ngram('quadgrams')
})
"""English ngram frequencies."""


ENGLISH_IC = _calculate_index_of_coincidence(english.unigrams, sum(english.unigrams.values()))
"""Index of coincidence for the English language."""
