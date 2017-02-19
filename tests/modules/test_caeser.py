"""Tests for the Caeser module."""
import pycipher
import os
import random
import string

from cckrypto.score_functions import (
    ngram, corpus
)
from cckrypto.modules import caesar
from cckrypto.util import remove


def _test_caesar(plaintext, score_functions, key=3):
    ciphertext = pycipher.Caesar(key).encipher(plaintext, keep_punct=True)
    decryptions = caesar.crack(
        ciphertext=ciphertext,
        score_functions=score_functions
    )

    print(decryptions)
    best_decryption = decryptions[0][0].upper()
    assert best_decryption == plaintext


def test_quick_brown_fox():
    """Testing quick brown fox."""
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    _test_caesar(plaintext, score_functions=[ngram.quadgram.score])


def test_defend_castle_wall():
    """Testing defend castle wall."""
    plaintext = "DEFEND THE EAST WALL OF THE CASTLE"
    _test_caesar(plaintext, score_functions=[ngram.quadgram.score])


# def test_buzz_buzz_buzz():
#     """Testing buzz buzz buzz."""
#     plaintext = "BUZZ BUZZ BUZZ"
#     _test_caesar(
#         plaintext,
#         score_functions=[
#             ngram.quadgram.score,
#             dictionary.score
#         ]
#     )

# def test_bye():
#     """Testing buzz buzz buzz."""
#     plaintext = "- BYE!"
#     _test_caesar(
#         plaintext,
#         score_functions=[
#             ngram.quadgram.score,
#             dictionary.score
#         ]
#     )

# def test_oh_my():
#     """Testing buzz buzz buzz."""
#     plaintext = "- OH, MY!"
#     _test_caesar(
#         plaintext,
#         score_functions=[
#             ngram.quadgram.score,
#             dictionary.score
#         ]
#     )

# def test_ok():
#     """Testing buzz buzz buzz."""
#     plaintext = "- OK."
#     _test_caesar(
#         plaintext,
#         score_functions=[
#             ngram.quadgram.score,
#             dictionary.score
#         ]
#     )


# # Aim for correct decryption in the top 10 decryptions with only quadram.
# def test_entire_bee_movie_quadgrams():
#     """Testing the entire bee move script."""
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     with open(os.path.join(dir_path, 'beemoviescript.txt')) as bee:
#         for line in bee:
#             plaintext = line.rstrip().upper()

#             # Skip lines which are too short
#             if len(remove(plaintext, string.punctuation + string.whitespace)) < 4:
#                 continue

#             # Encipher line using random Caesar cipher
#             ciphertext = pycipher.Caesar(
#                 random.randint(caesar.MIN_KEY, caesar.MAX_KEY)
#             ).encipher(plaintext, keep_punct=True)

#             # Use cckrypto to break it
#             decryptions = caesar.crack(
#                 ciphertext,
#                 score_functions=[ngram.quadgram.score]
#             )
#             top_ten = decryptions[0:10]
#             assert any(plaintext == d[0] for d in top_ten)


#Aim for correct decryption in the top 3 decryptions with quadgrams and dictionary
# def test_entire_bee_movie_dictionary():
#     """Testing the entire bee move script."""
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     with open(os.path.join(dir_path, 'beemoviescript.txt')) as bee:
#         for line in bee:
#             plaintext = line.rstrip().upper()

#             # Encipher line using random Caesar cipher
#             cipher = pycipher.Caesar(
#                 random.randint(caesar.MIN_KEY, caesar.MAX_KEY)
#             )
#             ciphertext = cipher.encipher(plaintext, keep_punct=True)

#             # Use cckrypto to break it
#             decryptions = caesar.crack(
#                 ciphertext,
#                 score_functions=[
#                     ngram.quadgram.score,
#                     corpus.english_words.score
#                 ]
#             )
#             top_three = decryptions[0:3]
#             if not any(plaintext == d[0] for d in top_three):
#                 print(plaintext)
#                 print(decryptions)
#                 # import sys
#                 # sys.exit()

#     assert 1 == 2
