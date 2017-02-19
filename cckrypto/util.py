"""Utility functions."""
import string

exclude = set(string.punctuation + string.whitespace)


def remove_punctuation(text):
    """Remove punctuation and whitespace."""
    text = ''.join(ch for ch in text if ch not in exclude)
    return text.rstrip()
