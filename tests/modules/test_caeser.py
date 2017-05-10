"""Tests for the Caeser module"""
import pytest

import pycipher

from lantern.modules import caesar
from lantern import fitness


def get_top_decryptions(decryptions, n):
    """Top N decryptions by score, not position"""
    top_decryptions = []
    index = 0
    next_score = 0

    while n > 0 and index <= len(decryptions) - 1:
        if decryptions[index].score < next_score:
            n -= 1

        top_decryptions.append(decryptions[index])
        index += 1

        if index >= len(decryptions):
            break

        next_score = decryptions[index].score

    return top_decryptions


def _test_caesar(plaintext, score_functions, key=3, top_n=1):
    ciphertext = pycipher.Caesar(key).encipher(plaintext, keep_punct=True)
    decryptions = caesar.crack(
        ciphertext=ciphertext,
        score_functions=score_functions
    )

    top_decryptions = get_top_decryptions(decryptions, top_n)

    print("Decryptions: ")
    for decrypt in decryptions:
        print(decrypt)
    print("Top Decryptions: ")
    for decrypt in top_decryptions:
        print(decrypt)

    match = None
    for decrypt in top_decryptions:
        if decrypt.plaintext.upper() == plaintext.upper():
            match = decrypt
            break

    assert match is not None
    assert match.key == key


def test_quick_brown_fox_unigrams():
    """Testing quick brown fox"""
    plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog"
    _test_caesar(plaintext, fitness.english.unigrams)


def test_quick_brown_fox_bigrams():
    """Testing quick brown fox"""
    plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog"
    _test_caesar(plaintext, fitness.english.bigrams)


def test_quick_brown_fox_trigrams():
    """Testing quick brown fox"""
    plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog"
    _test_caesar(plaintext, fitness.english.trigrams)


def test_quick_brown_fox_quadgrams():
    """Testing quick brown fox"""
    plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog"
    _test_caesar(plaintext, fitness.english.quadgrams)


def test_quick_brown_fox_upper():
    """Testing quick brown fox"""
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    _test_caesar(plaintext, fitness.english.quadgrams)


def test_quick_brown_fox_patristocrats():
    """Testing quick brown fox"""
    plaintext = "TheQu ckBro wnFox Jumps OverT heLaz yDog"
    _test_caesar(plaintext, fitness.english.quadgrams)


def test_quick_brown_fox_no_whitespace():
    """Testing quick brown fox"""
    plaintext = "thequickbrownfoxjumpsoverthelazydog"
    _test_caesar(plaintext, fitness.english.quadgrams)


def test_quick_brown_fox_no_whitespace_upper():
    """Testing quick brown fox"""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    _test_caesar(plaintext, fitness.english.quadgrams)


def test_defend_castle_wall():
    """Testing defend castle wall"""
    plaintext = "DEFEND THE EAST WALL OF THE CASTLE"
    _test_caesar(plaintext, fitness.english.quadgrams)


def test_buzz_buzz_buzz_quadgrams():
    """
    Testing buzz buzz buzz in top 2 results.
    haff haff haff beats it because it has a better freqency distribution.
    """
    plaintext = "BUZZ BUZZ BUZZ"
    _test_caesar(
        plaintext,
        score_functions=[
            fitness.english.quadgrams,
        ],
        top_n=2
    )


def test_narrow_key_range():
    """Test narrower keyrange lowers the amount of brute forcing done"""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    ciphertext = pycipher.Caesar(3).encipher(plaintext, keep_punct=True)

    decryptions = caesar.crack(ciphertext, fitness.english.quadgrams, min_key=3, max_key=5)
    assert len(decryptions) == 2
    assert decryptions[0].plaintext == plaintext


def test_invalid_key_range():
    """Test an invalid key throws ValueError"""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    ciphertext = pycipher.Caesar(3).encipher(plaintext, keep_punct=True)

    with pytest.raises(ValueError):
        caesar.crack(ciphertext, fitness.english.quadgrams, min_key=7, max_key=2)


def test_decrypt():
    """Test decrypt successfully decrypts ciphertext enciphered with the same key"""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    key = 3
    ciphertext = pycipher.Caesar(key).encipher(plaintext, keep_punct=True)
    assert caesar.decrypt(key, ciphertext) == plaintext


def test_decrypt_large_key_wrapped():
    """Test key value is wrapped around by the length of the alphabet"""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    key = 30
    ciphertext = pycipher.Caesar(key).encipher(plaintext, keep_punct=True)
    assert caesar.decrypt(key, ciphertext) == plaintext


# TODO: THIS NEEDS TO BE ACTIVATED ONCE CORPUS IS FIXED
# def test_buzz_buzz_buzz_quadgrams_and_corpus():
#     """
#     Testing buzz buzz buzz in top 2 results.
#     haff haff haff beats it because of a better freqency distribution.
#     """
#     plaintext = "BUZZ BUZZ BUZZ"
#     _test_caesar(
#         plaintext,
#         score_functions=[
#             fitness.english.quadgrams,
#         ],
#         top_n=2
#     )


# def test_bye():
#     """Testing Bye has top score"""
#     plaintext = "- BYE!"
#     _test_caesar(
#         plaintext,
#         score_functions=[
#             fitness.english.quadgrams,
#             partial(corpus.english_words, whitespace_hint=True)
#         ]
#     )


# def test_oh_my():
#     """
#     Testing oh my in top 2 positions.

#     un se as a decryption beats out oh my.
#     Can be fixed with better corpus.
#     """
#     plaintext = "- OH, MY!"
#     _test_caesar(
#         plaintext,
#         score_functions=[
#             fitness.english.quadgrams,
#             partial(corpus.english_words, whitespace_hint=True)
#         ],
#         top_n=2
#     )


# def test_ok():
#     """Testing ok"""
#     plaintext = "- OK."
#     _test_caesar(
#         plaintext,
#         score_functions=[
#             fitness.english.quadgrams,
#             partial(corpus.english_words, whitespace_hint=True)
#         ]
#     )


# TODO: DO I NEED THIS TEST ANYMORE? NOT REALLY A UNIT TEST....
# def test_entire_bee_movie_quadgrams():
#     """
#     Encrpyt and decrypt bee movie script only using ngram analysis.

#     Correct decryption in top 2 rankings.
#     """
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     with open(os.path.join(dir_path, '../util', 'beemoviescript.txt')) as bee:
#         for line in bee:
#             _test_caesar(
#                 line.rstrip().upper(),
#                 score_functions=[fitness.english.quadgrams],
#                 top_n=2
#             )


# def test_entire_bee_movie_quadgrams_and_corpus():
#     """
#     Encrpyt and decrypt bee movie script using ngram and corpus analysis.

#     Correct decryption 1st rank every time.
#     """
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     with open(os.path.join(dir_path, '../util', 'beemoviescript.txt')) as bee:
#         for line in bee:
#             _test_caesar(
#                 line.rstrip().upper(),
#                 score_functions=[
#                     ngram.quadgram,
#                     partial(corpus.english_words, whitespace_hint=True)
#                 ],
#                 top_n=1
#             )
