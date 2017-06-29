"""Class to dynamically create attributes only when they are needed.

Todo:
    This needs some more functionality. Specifically it doesnt behave like a
    proper dictionary
"""


class DynamicDict:
    """Dictionary which builds values when they are accessed for the first time.

    Example:
        >>> ngrams = DynamicDict({
        ...     'trigrams': lambda: load_ngrams('trigrams'),
        ...     'quadgrams': lambda: load_ngrams('quadgrams')
        ... })

    Since trigrams and quadgrams are large files, its expensive to load them in
    if theyre not needed. Using the DynamicDict ensures they are only loaded when
    they are accessed for the first time.
    """

    def __init__(self, builders={}):
        """Instantiate dict with mapping of keys to builders.

        Args:
            builders (dict): key to function mapping
        """
        self.builders = builders

    def __getattr__(self, name):
        """Attempt to build values that are not already created."""
        try:
            attribute = self.builders[name]()
        except KeyError:
            raise AttributeError("'DynamicDict' object has no attribute '{}'".format(name))
        else:
            setattr(self, name, attribute)
            return attribute
