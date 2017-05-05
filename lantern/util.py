"""Utility functions."""

import string


def remove(text, exclude):
    """Remove exclude symbols from text."""
    try:
        return text.translate(None, exclude)
    except TypeError:
        return text.translate(str.maketrans('', '', exclude))


def split_columns(text, n_cols):
    return [text[i::n_cols] for i in range(n_cols)]


def combine_columns(columns):
    return ''.join(x for zipped in zip(*columns) for x in zipped)
