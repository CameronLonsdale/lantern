"""
Scoring algorithm to return probability of correct decryption.
Output range depends on the score functions used.
"""


def score(text, scoring_functions):
    """
    Score ``text`` using ``scoring_functions``.

    Examples: ::

        score("abc", function_a)
        score("abc", [function_a, function_b])

    Parameters:
        text (str): The text to score
        scoring_functions (Function or iterable of functions): Function(s) to score text with
    
    Return:
        Arithmetic mean of scores
    """
    if not hasattr(scoring_functions, '__iter__'):
        scoring_functions = [scoring_functions]

    total_score = sum((func(text) for func in scoring_functions))
    return total_score / len(scoring_functions)
