"""Utility functions."""

import string


def remove(text, exclude):
    """Remove letters from exclude in text."""
    return ''.join(ch for ch in text if ch not in exclude).rstrip()


def remove_punct_and_whitespace(text):
    """Remove punctuation and whitespace from a string."""
    return remove(text, string.punctuation + string.whitespace)


def remove_punctuation(text):
    """Remove punctuation and whitespace."""
    return remove(text, string.punctuation)


def remove_whitespace(text):
    """Remove whitespace from text."""
    return remove(text, string.whitespace)


def break_columns(ciphertext, key_length):
    return [ciphertext[i::key_length] for i in range(key_length)]


def combine_columns(columns):
    return ''.join(x for zipped in zip(*columns) for x in zipped)
