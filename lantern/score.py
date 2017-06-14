"""
Scoring algorithm to return probability of correct decryption.
Output range depends on the score functions used.
"""


def score(text, score_function, *args):
    """
    Score ``text`` using score functions.

    Examples: ::

        score("abc", function_a)
        score("abc", function_a, function_b)

    Arguments:
        text (str): The text to score
        score_function (function): function to score with
        args (variable length arg list): Additional functions to use

    Return:
        Arithmetic mean of scores
    """
    scoring_functions = (score_function, *args)
    total_score = sum(func(text) for func in scoring_functions)
    return total_score / len(scoring_functions)
