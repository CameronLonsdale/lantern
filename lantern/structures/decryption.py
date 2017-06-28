"""Class to group information about a decryption.

Todo:
    Possibly add more functionality to this class
    * Equality checking
    * Formatted plaintext (added spaces)
    Once there is evidence these things are needed, I will implement them
"""


class Decryption:
    """A decryption object, composed of plaintext, a score and the key.

    Example:
        >>> decryption = Decryption("example", "key", -10)
        >>> decryption.plaintext
        example
        >>> decryption.key
        key
        >>> decryption.score
        -10
    """

    def __init__(self, plaintext, key, score):
        """
        Args:
            plaintext: The decrypted ciphertext
            key: The key which resulted in this decryption
            score: The score of this decryption
        """
        self.plaintext = plaintext
        self.key = key
        self.score = score

    def __str__(self):
        """Return the plaintext as the string representation for the object.

        Returns:
            plaintext
        """
        return self.plaintext

    def __lt__(self, other):
        """Compare decryptions with other decryptions by score.

        Args:
            other: Object to compare with

        Returns:
            True if self is less than other, else False
        """
        return self.score < other.score
