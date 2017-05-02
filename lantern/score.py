"""
Scoring algorithm to return probability of correct decryption.
Output Range depends on the score functions used.
"""


def score(plaintext, scoring_functions):
    """
    Score plaintext using scoring_functions.
    Final result is a weighted mean.
    """
    if not hasattr(scoring_functions, '__iter__'):
        scoring_functions = [scoring_functions]

    total_score = sum((func(plaintext) for func in scoring_functions))
    return total_score / len(scoring_functions)
