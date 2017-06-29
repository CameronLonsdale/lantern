"""Dynamic Dictionary"""


class DynamicDict(dict):
    """Dictionay which builds values when they are accessed for the first time

    Todo:
        This does not work exactly as it should. However my brain is not working
        to fix it up so I will come back later.
    """
    def __init__(self, builders={}):
        self.builders = builders

    def __getattr__(self, name):
        """Exaplanation"""
        try:
            attribute = self.builders[name]()
        except KeyError:
            raise AttributeError("'DynamicDict' object has no attribute '{}'".format(name))
        else:
            setattr(self, name, attribute)
            return attribute
