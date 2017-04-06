"""Testing the scoring algorithm"""

from cckrypto.score import score


def test_score_with_multiple_functions():
    """Plaintext scored with two functions"""
    plaintext = "lorem ipsum"
    assert score(
        plaintext,
        scoring_functions=[
            lambda x: 0,
            lambda y: 0
        ]
    ) == 0


def test_score_is_averaged():
    """Score is averaged over number of functions used"""
    plaintext = "lorem ipsum"
    assert score(
        plaintext,
        scoring_functions=[
            lambda x: -10,
            lambda y: -20
        ]
    ) == -15


def test_score_is_averaged_positive_and_negative():
    """Score is averaged over number of functions used"""
    plaintext = "lorem ipsum"
    assert score(
        plaintext,
        scoring_functions=[
            lambda x: -10,
            lambda y: 0
        ]
    ) == -5
