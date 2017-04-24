"""Class to group information about a decryption"""


class Decryption():
    """Computes the score of a text by using the calculated probabilities from a loaded ngramfile."""

    def __init__(self, plaintext, key, score):
        self.plaintext = plaintext
        self.key = key
        self.score = score
