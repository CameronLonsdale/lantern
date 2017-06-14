"""Testing the corpus score fuction"""

from math import log10

from lantern.fitness import Corpus


def _test_corpus_constructor(words):
    corpus = Corpus(words)
    assert corpus.words == words
    assert corpus.floor == log10(0.01 / len(words))


def test_corpus_constructor_with_set():
    """Test corpus constructor with set"""
    words = set(["hello", "other", "english", "words"])
    _test_corpus_constructor(words)


def test_corpus_constructor_with_list():
    """Test corpus constructor with list"""
    words = ["hello", "other", "english", "words"]
    _test_corpus_constructor(words)


def test_corpus_all_english_one_word():
    """Test english words returns 0 score"""
    english_scorer = Corpus(set(["hello", "other", "english", "words"]))
    plaintext = "Hello"
    assert english_scorer(plaintext) == 0


def test_corpus_one_non_english():
    """Test incorrect words get assigned floor value"""
    english_scorer = Corpus(set(["hello", "other", "english", "words"]))
    plaintext = "jiugyfti"
    assert english_scorer(plaintext) == 1 * english_scorer.floor


def test_corpus_multiple_non_english():
    """Test incorrect scores compound"""
    english_scorer = Corpus(set(["hello", "other", "english", "words"]))
    plaintext = "jiugyfti ikomoipa"
    assert english_scorer(plaintext) == 2 * english_scorer.floor
