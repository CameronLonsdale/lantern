"""
Utility functions to format and marshal data.
"""

import itertools


def remove(text, exclude):
    """
    Remove ``exclude`` symbols from ``text``

    Example: ::

        remove("example text", string.whitespace) == "exampletext"

    :param str text: The text to modify
    :param iterable exclude: symbols to exclude
    :return: text with exclude symbols removed
    """
    exclude = ''.join(str(symbol) for symbol in exclude)

    try:
        return text.translate(None, exclude)
    except TypeError:
        return text.translate(str.maketrans('', '', exclude))


def split_columns(text, n_cols):
    """
    split ``text`` into ``n_cols`` number of columns

    Example: ::

        split_columns("example", 2) == ['eape', 'xml']

    :param str text: The text to split
    :param int n_cols: number of columns
    :return: list of columns
    """
    n_cols = max(1, min(len(text), n_cols))
    return [text[i::n_cols] for i in range(n_cols)]


def combine_columns(columns):
    """
    combine ``columns`` into a single string

    Example: ::

        combine_columns(['eape', 'xml']) == "example"

    :param iterable columns: ordered columns to combine
    :return: string of combined columns
    """
    try:
        columns_zipped = itertools.zip_longest(*columns) 
    except AttributeError:
        columns_zipped = itertools.izip_longest(*columns) 
    
    return ''.join(x for zipped in columns_zipped for x in zipped if x)
