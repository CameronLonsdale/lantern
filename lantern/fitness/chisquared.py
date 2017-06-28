"""Chi Squared Scoring function."""

from lantern.analysis.frequency import frequency_analyze, chi_squared


class ChiSquared:
    """Score a text by comparing its frequency distribution against another.

    Note:
        It is easy to be penalised without knowing it when using this scorer.
        English frequency ngrams are capital letters, meaning when using it
        any text you score against must be all capitals for it to give correct results.
        I am aware of the issue and will work on a fix.

    Todo:
        Maybe include paramter for ngram size. Havent had a use case for this yet.
        Once there is evidence it is needed, I will add it.
    """

    def __init__(self, target_frequency):
        """
        Args:
            target_frequency (dict): symbol to frequency mapping of the distribution to compare with
        """
        self.target_frequency = target_frequency

    def __call__(self, text):
        """Score text using the Chi Squared statistic.

        Example:
            >>> fitness = ChiSquared(english.unigrams)
            >>> fitness("ABC")
            -32.2

        Args:
            text (str): The text to score

        Returns:
            Chi Squared score for text
        """
        return -chi_squared(frequency_analyze(text), self.target_frequency)
