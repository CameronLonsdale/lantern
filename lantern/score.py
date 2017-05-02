"""
Scoring algorithm to return probability of correct decryption.
Output range depends on the score functions used.
"""


def score(text, scoring_functions):
    """
    Score ``text`` using ``scoring_functions``

    Example: ::

        score("abc", function_a)
        score("abc", [function_a, function_b])

    :param str text: The text to score
    :param scoring_functions: Function(s) to score text with
    :type scoring_functions: Function or list of functions
    :return: Mean of scores
    """
    if not hasattr(scoring_functions, '__iter__'):
        scoring_functions = [scoring_functions]

    total_score = sum((func(text) for func in scoring_functions))
    return total_score / len(scoring_functions)
