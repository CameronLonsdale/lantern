"""Tests for the Caeser module"""
import pycipher
import os
import random

from functools import partial

from lantern.modules import caesar
from lantern import fitness


def _test_caesar(plaintext, score_functions, key=3, top_n=1):
    ciphertext = pycipher.Caesar(key).encipher(plaintext, keep_punct=True)
    decryptions = caesar.crack(
        ciphertext=ciphertext,
        score_functions=score_functions
    )

    # Top N decryptions by score, not position
    top_decryptions = []
    index = 0
    next_score = 0

    while top_n > 0 and index < len(decryptions) - 1:
        if decryptions[index].score < next_score:
            top_n -= 1

        top_decryptions.append(decryptions[index])
        next_score = decryptions[index + 1].score
        index += 1

    print("Decryptions: " + str(decryptions))
    print("Top Decryptions: " + str(top_decryptions))
    assert any(plaintext.upper() == d.plaintext.upper() for d in top_decryptions)


def test_quick_brown_fox():
    """Testing quick brown fox"""
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    _test_caesar(plaintext, fitness.english.quadgrams)


def test_defend_castle_wall():
    """Testing defend castle wall"""
    plaintext = "DEFEND THE EAST WALL OF THE CASTLE"
    _test_caesar(plaintext, fitness.english.quadgrams)


# def test_buzz_buzz_buzz():
#     """
#     Testing buzz buzz buzz in top 3 results.

#     haff haff haff beats it because of a better freqency distribution and its also a word.

#     Way to correct this would be to use a more specialised corpus.
#     """
#     plaintext = "BUZZ BUZZ BUZZ"
#     _test_caesar(
#         plaintext,
#         score_functions=[
#             fitness.english.quadgrams,
#             partial(corpus.english_words, whitespace_hint=True)
#         ],
#         top_n=3
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


def test_entire_bee_movie_quadgrams():
    """
    Encrpyt and decrypt bee movie script only using ngram analysis.

    Correct decryption in top 2 rankings.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, '../util', 'beemoviescript.txt')) as bee:
        for line in bee:
            _test_caesar(
                line.rstrip().upper(),
                score_functions=[fitness.english.quadgrams],
                top_n=2
            )


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
