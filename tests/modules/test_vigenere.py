"""Tests for the Simple Substitution module"""
import pytest

import pycipher
import random
import string

from lantern.modules import vigenere
from lantern import fitness, analysis
from lantern.util import remove


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


def _test_vigenere(plaintext, score_functions, key, period=None, top_n=1):
    ciphertext = pycipher.Vigenere(key).encipher(plaintext)
    decryptions = vigenere.crack(
        ciphertext=ciphertext,
        score_functions=score_functions,
        key_period=period
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
        if decrypt.plaintext.upper() == remove(plaintext.upper(), string.punctuation + string.whitespace):
            match = decrypt
            break

    assert match is not None
    # assert match.key == ''.join(key)
    # TODO I THINK THIS IS BROKEN


# def test_50_character_text():
#     """Testing text of length ~50"""
#     plaintext = """Compute the probability of text being a valid string"""

#     key = list(string.ascii_uppercase)
#     random.shuffle(key)
#     _test_simplesubstitution(
#         plaintext.upper(),
#         score_functions=[ngram.quadgram],
#         key=key
#     )

# ITS ALMOST AT 100% accurancy, but sometimes doesnt work so I should try testing if its correct by using a hamming distance and make sure its below a certain threshold?
# Ie. 1 or 2 letters wrong would be sufficient. Maximum 4.
# def test_100_character_text():
#     """Testing text of length ~100"""
#     plaintext = """I think importance of talking about what you know is a moral obligation to fill the space with knowledge"""
#     _test_simplesubstitution(
#         plaintext,
#         [fitness.english.bigrams, fitness.english.quadgrams],
#         ntrials=100
#     )


def test_250_character_text_periods_unknown():
    """Testing text of length ~25, many different periods, none given to cracker"""
    plaintext = """Almost all of the game's cut-scenes are done in a stick puppet style. The game begins with the narrator (voiced by Will Stamper) telling the adventures of the hundreds of friends aboard the S.S. Friendship, as well as Hatty Hattington, who is known as "best friend to one and all"."""
    for period in range(1, 10):
        key = list(string.ascii_uppercase)
        random.shuffle(key)
        key = key[:period]

        _test_vigenere(
            plaintext,
            [fitness.ChiSquared(analysis.frequency.english.unigrams),
             fitness.english.quadgrams],
            key=key,
        )


def test_250_character_text_periods_known():
    """Testing text of length ~25, many different periods, none given to cracker"""
    plaintext = """Almost all of the game's cut-scenes are done in a stick puppet style. The game begins with the narrator (voiced by Will Stamper) telling the adventures of the hundreds of friends aboard the S.S. Friendship, as well as Hatty Hattington, who is known as "best friend to one and all"."""
    for period in range(1, 10):
        key = list(string.ascii_uppercase)
        random.shuffle(key)
        key = key[:period]

        _test_vigenere(
            plaintext,
            [fitness.ChiSquared(analysis.frequency.english.unigrams),
             fitness.english.quadgrams],
            key=key,
            period=period
        )


def test_500_character_text_all_periods_unknown():
    """Testing text of length ~500, many different periods, none given to cracker"""
    plaintext = """Upon its release, the novel received near universal acclaim. Although Dickens' contemporary Thomas Carlyle referred to it disparagingly as that "Pip nonsense," he nevertheless reacted to each fresh instalment with "roars of laughter."Later, George Bernard Shaw praised the novel, as "All of one piece and consistently truthful." During the serial publication, Dickens was pleased with public response to Great Expectations and its sales; when the plot first formed in his mind, he called it "a very fine, new and grotesque idea."""
    for period in range(1, 10):
        key = list(string.ascii_uppercase)
        random.shuffle(key)
        key = key[:period]

        _test_vigenere(
            plaintext,
            [fitness.ChiSquared(analysis.frequency.english.unigrams),
             fitness.english.quadgrams],
            key=key
        )


def test_500_character_text_all_periods_known():
    """Testing text of length ~500, many different periods, none given to cracker"""
    plaintext = """Upon its release, the novel received near universal acclaim. Although Dickens' contemporary Thomas Carlyle referred to it disparagingly as that "Pip nonsense," he nevertheless reacted to each fresh instalment with "roars of laughter."Later, George Bernard Shaw praised the novel, as "All of one piece and consistently truthful." During the serial publication, Dickens was pleased with public response to Great Expectations and its sales; when the plot first formed in his mind, he called it "a very fine, new and grotesque idea."""
    for period in range(1, 10):
        key = list(string.ascii_uppercase)
        random.shuffle(key)
        key = key[:period]

        _test_vigenere(
            plaintext,
            fitness.ChiSquared(analysis.frequency.english.unigrams),
            key=key,
            period=period
        )


# TEST VIGENERE INVALID PERIOD


def test_decrypt():
    """Test decrypt successfully decrypts ciphertext enciphered with the same key"""
    assert vigenere.decrypt("KEY", "RIJVS") == "HELLO"


def test_decrypt_as_list():
    """Test decrypt successfully decrypts ciphertext enciphered with the same key"""
    assert vigenere.decrypt(list("KEY"), "RIJVS") == "HELLO"
