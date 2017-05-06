"""Class to group information about a decryption"""


class Decryption():
    """
    A decryption object, composed of plaintext, a score and the key

    Example: ::

        decryption = Decryption("plaintext", "key", -10)
        decryption.plaintext == "plaintext"
        decryption.key == "key"
        decryption.score == -10

    :param object plaintext: The decrypted ciphertext
    :param object key: The key which resulted in this decryption
    :param number score: The score of this decryption
    """

    def __init__(self, plaintext, key, score):
        self.plaintext = plaintext
        self.key = key
        self.score = score

    def __str__(self):
        """
        Return the plaintext as the string representation for the object

        :return: self.plaintext
        """
        return self.plaintext

    def __lt__(self, other):
        """
        Compare decryptions with other decryptions by score

        :param object other: object to compare with
        :return: True or False
        """
        return self.score < other.score
