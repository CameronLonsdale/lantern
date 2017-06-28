"""Fitness scoring using pattern matching."""

import re


class PatternMatch():
    """Computes the score of a text by determing if a pattern matches."""

    def __init__(self, regex):
        """Accept a regex as a pattern to match text on.

        Args:
            regex (str): regular expression string to use as a pattern
        """
        self.pattern = re.compile(regex)

    def __call__(self, text):
        """Score text based on whether a match is found in the text.

        Example:
            >>> fitness = PatternMatch("flag{.*}")
            >>> fitness("flag{example}")
            0

            >>> fitness("junk")
            -1

        Args:
            text (str): The text to score

        Returns:
            0 if pattern maches else -1
        """
        return -1 if self.pattern.search(text) is None else 0
