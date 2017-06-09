"""Utility functions to format and marshal data."""

import itertools


def remove(text, exclude):
    """
    Remove ``exclude`` symbols from ``text``.

    Example: ::

        remove("example text", string.whitespace) == "exampletext"

    Parameters:
        text (str): The text to modify
        exclude (iterable): The symbols to exclude

    Return:
        text with exclude symbols removed
    """
    exclude = ''.join(str(symbol) for symbol in exclude)
    return text.translate(str.maketrans('', '', exclude))


def split_columns(text, n_cols):
    """
    Split ``text`` into ``n_cols`` number of columns.

    Example: ::

        split_columns("example", 2) == ['eape', 'xml']

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


def combine_columns(first, *rest):
    """
    Combine ``columns`` into a single string.

    Example: ::

        combine_columns('eape', 'xml') == "example"

    Parameters:
        columns (variable length arg list): Ordered iterable of columns to combine

    Return:
        string of combined columns
    """
    columns_zipped = itertools.zip_longest(first, *rest)
    return ''.join(x for zipped in columns_zipped for x in zipped if x)
