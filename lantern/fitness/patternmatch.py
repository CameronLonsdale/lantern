"""Fitness scoring using pattern matching."""

import re


def PatternMatch(regex):
    """Compute the score of a text by determing if a pattern matches.

    Example:
        >>> fitness = PatternMatch("flag{.*}")
        >>> fitness("flag{example}")
        0

        >>> fitness("junk")
        -1

    Args:
        regex (str): regular expression string to use as a pattern
    """
    pattern = re.compile(regex)
    return lambda text: -1 if pattern.search(text) is None else 0
