"""Chi Squared Scoring function."""

from lantern.analysis.frequency import frequency_analyze, chi_squared


def ChiSquared(target_frequency):
    """Score a text by comparing its frequency distribution against another.

    Note:
        It is easy to be penalised without knowing it when using this scorer.
        English frequency ngrams are capital letters, meaning when using it
        any text you score against must be all capitals for it to give correct results.
        I am aware of the issue and will work on a fix.

    Todo:
        Maybe include paramter for ngram size. Havent had a use case for this yet.
        Once there is evidence it is needed, I will add it.

    Example:
        >>> fitness = ChiSquared(english.unigrams)
        >>> fitness("ABC")
        -32.2

    Args:
        target_frequency (dict): symbol to frequency mapping of the distribution to compare with
    """
    def inner(text):
        text = ''.join(text)
        return -chi_squared(frequency_analyze(text), target_frequency)

    return inner
