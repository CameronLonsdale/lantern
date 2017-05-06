"""
Utility functions to format and marshal data.
"""

from itertools import zip_longest


def remove(text, exclude):
    """
    Remove ``exclude`` symbols from ``text``

    Example: ::

        remove("example text", string.whitespace) == "exampletext"

    :param str text: The text to modify
    :param str exclude: String of symbols to exclude
    :return: text without symbols in exclude
    """
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
    :raises ValueError: if n_cols is <= 0 or > len(text)
    """
    if n_cols <= 0 or n_cols > len(text):
        raise ValueError("Invalid argument n_cols {}".format(n_cols))

    return [text[i::n_cols] for i in range(n_cols)]


def combine_columns(columns):
    """
    combine iterable of ``columns`` into a single string

    Example: ::

        combine_columns(['eape', 'xml']) == "example"

    :param iterable columns: ordered iterable of columns
    :return: string of combined columns
    """
    return ''.join(x for zipped in zip_longest(*columns) for x in zipped if x is not None)
