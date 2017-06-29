"""Utility functions to format and marshal data."""

import itertools


def remove(text, exclude):
    """Remove ``exclude`` symbols from ``text``.

    Example:
        >>> remove("example text", string.whitespace)
        'exampletext'

    Args:
        text (str): The text to modify
        exclude (iterable): The symbols to exclude

    Returns:
        ``text`` with ``exclude`` symbols removed
    """
    exclude = ''.join(str(symbol) for symbol in exclude)
    return text.translate(str.maketrans('', '', exclude))


def split_columns(text, n_columns):
    """Split ``text`` into ``n_columns`` many columns.

    Example:
        >>> split_columns("example", 2)
        ['eape', 'xml']

    Args:
        text (str): The text to split
        n_columns (int): The number of columns to create

    Returns:
        List of columns

    Raises:
        ValueError: If n_cols is <= 0 or >= len(text)
    """
    if n_columns <= 0 or n_columns > len(text):
        raise ValueError("n_columns must be within the bounds of 1 and text length")

    return [text[i::n_columns] for i in range(n_columns)]


def combine_columns(columns):
    """Combine ``columns`` into a single string.

    Example:
        >>> combine_columns(['eape', 'xml'])
        'example'

    Args:
        columns (iterable): ordered columns to combine

    Returns:
        String of combined columns
    """
    columns_zipped = itertools.zip_longest(*columns)
    return ''.join(x for zipped in columns_zipped for x in zipped if x)


def iterate_ngrams(text, n):
    """Generator to yield ngrams in ``text``.

    Example:
        >>> for ngram in iterate_ngrams("example", 4):
        ...     print(ngram)
        exam
        xamp
        ampl
        mple

    Args:
        text (str): text to iterate over
        n (int): size of window for iteration

    Returns:
        Generator expression to yield the next ngram in the text

    Raises:
        ValueError: If n is non positive
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")

    return [text[i: i + n] for i in range(len(text) - n + 1)]


def group(text, size):
    """Group ``text`` into blocks of ``size``.

    Example:
        >>> group("test", 2)
        ['te', 'st']

    Args:
        text (str): text to separate
        size (int): size of groups to split the text into

    Returns:
        List of n-sized groups of text

    Raises:
        ValueError: If n is non positive
    """
    if size <= 0:
        raise ValueError("n must be a positive integer")

    return [text[i:i + size] for i in range(0, len(text), size)]
