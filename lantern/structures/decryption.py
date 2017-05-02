"Class to group information about a decryption"


class Decryption():
    """
    Structure to group data about a decryption.
    Included are the plaintext, the corresponding key, and the score given to this plaintext
    """

    def __init__(self, plaintext, key, score):
        self.plaintext = plaintext
        self.key = key
        self.score = score

    def __str__(self):
        return self.plaintext

    def __lt__(self, other):
        return self.score < other.score
