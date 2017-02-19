"""
Scoring algorithm to return probability of correct decryption.

Scores range from -inf to 0 due to log probability.

A score of 0 indicates correct plaintext.
"""


def score(plaintext, scoring_functions):
    """
    Score plaintext using scoring_functions.

    Final result is a weighted mean.
    TODO: Support custom weights?
    """
    total_score = sum((func(plaintext) for func in scoring_functions))
    return total_score / len(scoring_functions)
