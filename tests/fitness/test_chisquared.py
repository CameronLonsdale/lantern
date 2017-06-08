"""Test the chi-squared scoring function"""

from lantern.fitness import ChiSquared


def test_chisquared():
    scorer = ChiSquared({'a': 1, 'b': 2})
    text = 'aabbb'
    assert scorer(text) == -0.1

# TODO: solve the floating point inaccuracy problem
# def test_chisquared_english_unigrams():
#     unigram_freq = frequency_to_probability(english.unigrams)
#     scorer = ChiSquared(english.unigrams)

#     # TODO: This should be replaced by using the keep_punct flag once its added
#     text = "This is an example".upper().replace(' ', '')
#     assert scorer(text) == -chi_squared(frequency_analyze(text), unigram_freq)
