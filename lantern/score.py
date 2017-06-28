"""
Scoring algorithm to return probability of correct decryption.
Output range depends on the score functions used.
"""

import statistics


def score(text, *score_functions):
    """Score ``text`` using ``score_functions``.

    Examples:
        >>> score("abc", function_a)
        >>> score("abc", function_a, function_b)

    Args:
        text (str): The text to score
        *score_functions (variable length argument list): functions to score with

    Returns:
        Arithmetic mean of scores

    Raises:
        ValueError: If score_functions is empty
    """
    if not score_functions:
        raise ValueError("score_functions must not be empty")

    return statistics.mean(func(text) for func in score_functions)
