"""Class to group information about a decryption"""


class Decryption():
    """A decryption object, composed of plaintext, a score and the key.

    Example:
        >>> decryption = Decryption("plaintext", "key", -10)
        >>> decryption.plaintext
        plaintext
        >>> decryption.key
        key
        >>> decryption.score
        -10
    """

    def __init__(self, plaintext, key, score):
        """
        Parameters:
            plaintext (str): The decrypted ciphertext
            key (object): The key which resulted in this decryption
            score (object): The score of this decryption
        """
        self.plaintext = plaintext
        self.key = key
        self.score = score

    def __str__(self):
        """Return the plaintext as the string representation for the object.

        Return:
            self.plaintext
        """
        return self.plaintext

    def __lt__(self, other):
        """Compare decryptions with other decryptions by score.

        Parameters:
            other (object): Object to compare with

        Return:
            True or False
        """
        return self.score < other.score
