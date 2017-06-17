"""
Scoring algorithm to return probability of correct decryption.
Output range depends on the score functions used.
"""


def score(text, *score_functions):
    """
    Score ``text`` using score functions.

    Examples: ::

        score("abc", function_a)
        score("abc", function_a, function_b)

    Parameters:
        text (str): The text to score
        score_functions (variable length arg list): functions to score with

    Return:
        Arithmetic mean of scores

    Raises:
        ValueError: If score_functions is empty
    """
    if not score_functions:
        raise ValueError("score_functions must not be empty")

    total_score = sum(func(text) for func in score_functions)
    return total_score / len(score_functions)
