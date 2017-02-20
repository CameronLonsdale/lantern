"""Testing the corpus score fuction."""
from cckrypto.score_functions.corpus import Corpus
from nltk.corpus import words
from math import log10


def test_corpus_constructor():
    """Test corpus constructor is correct."""
    english = Corpus(words.words())
    assert english.words == words.words()
    assert english.floor == log10(0.01 / len(words.words()))


def test_corpus_all_english_one_word():
    """Test english words returns 0 score."""
    english = Corpus(words.words())
    plaintext = "Hello"
    assert english.score(
        plaintext,
        whitespace_hint=True
    ) == 0


def test_corpus_one_non_english():
    """Test incorrect words get assisgned floor value."""
    english = Corpus(words.words())
    plaintext = "jiugyfti"
    assert english.score(
        plaintext,
        whitespace_hint=True
    ) == 1 * english.floor


def test_corpus_multiple_non_english():
    """Test incorrect scores compound."""
    english = Corpus(words.words())
    plaintext = "jiugyfti ikomoipa"
    assert english.score(
        plaintext,
        whitespace_hint=True
    ) == 2 * english.floor


def test_corpus_english_no_whitespace_hint():
    """Test whitespace infered with option."""
    english = Corpus(words.words())
    plaintext = "Hellofriend."
    assert english.score(
        plaintext,
        whitespace_hint=False
    ) == 0
