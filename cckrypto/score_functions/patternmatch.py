"""Fitness scoring using pattern matching."""
import re


class PatternMatch():
    """Computes the score of a text by determing if a pattern matches."""

    def __init__(self, regex):
        """Accept a regex as a pattern to match text on."""
        self.pattern = re.compile(regex)

    def __call__(self, text):
        """Score text based on whether a match is found in the text."""
        return -1 if self.pattern.search(text) is None else 0
