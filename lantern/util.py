"""Utility functions to format and marshal data."""

import itertools


def remove(text, exclude):
    """Remove ``exclude`` symbols from ``text``.

    Example:
        >>> remove("example text", string.whitespace)
        'exampletext'

    Parameters:
        text (str): The text to modify
        exclude (iterable): The symbols to exclude

    Return:
        text with exclude symbols removed
    """
    exclude = ''.join(str(symbol) for symbol in exclude)
    return text.translate(str.maketrans('', '', exclude))


def split_columns(text, n_cols):
    """Split ``text`` into ``n_cols`` number of columns.

    Example:
        >>> split_columns("example", 2)
        ['eape', 'xml']

    Parameters:
        text (str): The text to split
        n_cols (int): The number of columns to create

    Return:
        list of columns

    Raises:
        ValueError: If n_cols is <= 0 or >= len(text)
    """
    if n_cols <= 0 or n_cols > len(text):
        raise ValueError("n_cols must be within the bounds of 1 and text length")

    return [text[i::n_cols] for i in range(n_cols)]


def combine_columns(*columns):
    """Combine ``columns`` into a single string.

    Example:
        >>> combine_columns('eape', 'xml')
        'example'

    Parameters:
        columns (variable length arg list): columns to combine

    Return:
        string of combined columns

    Raises:
        ValueError: If columns is empty
    """
    if not columns:
        raise ValueError("columns must not be empty")

    columns_zipped = itertools.zip_longest(*columns)
    return ''.join(x for zipped in columns_zipped for x in zipped if x)


def iterate_ngrams(text, n):
    """Generator to yield ngrams in text.

    Example:
        >>> for ngram in iterate_ngrams("example", 4):
        ...     print(ngram)
        exam
        xamp
        ampl
        mple

    Parameters:
        text (str): text to iterate over
        n (int): size of window for iteration

    Yields:
        The next ngram in the text

    Raises:
        ValueError: If n is non positive
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")

    for i in range(len(text) - n + 1):
        yield text[i: i + n]


def group(text, n):
    """Group text into blocks of n.

    Example:
        >>> group("test", 2)
        ['te', 'st']

    Parameters:
        text (str): text to separate
        n (int): size of groups to split the text into

    Returns:
        list of n-sized groups of text

    Raises:
        ValueError: If n is non positive
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")

    return [text[i:i + n] for i in range(0, len(text), n)]
