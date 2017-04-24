"""Tests for the Simple Substitution module"""
import pycipher
import random
import string

from lantern.modules import simplesubstitution

from lantern.score_functions import (
    english_scorer, corpus
)


def _test_simplesubstitution(plaintext, score_functions, key, top_n=1):
    ciphertext = pycipher.SimpleSubstitution(key).encipher(plaintext, keep_punct=True)
    decryptions = simplesubstitution.crack(
        ciphertext=ciphertext,
        score_functions=score_functions
    )

    # Top N decryptions by score, not position
    top_decryptions = []
    index = 0
    next_score = 0

    while top_n > 0 and index <= len(decryptions) - 1:
        if decryptions[index].score < next_score:
            top_n -= 1

        top_decryptions.append(decryptions[index])
        index += 1

        if index >= len(decryptions):
            break

        next_score = decryptions[index].score

    print("Decryptions: " + str(decryptions))
    print("Top Decryptions: " + str(top_decryptions))
    assert any(plaintext.upper() == d.plaintext.upper() for d in top_decryptions)


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


# def test_100_character_text():
#     """Testing text of length ~100"""
#     plaintext = """I think importance of talking about what you know is a moral obligation to fill the space with knowledge"""

#     key = list(string.ascii_uppercase)
#     random.shuffle(key)
#     _test_simplesubstitution(
#         plaintext.upper(),
#         score_functions=[ngram.quadgram()],
#         key=key
#     )


def test_250_character_text():
    """Testing text of length ~250"""
    plaintext = """Almost all of the game's cut-scenes are done in a stick puppet style. The game begins with the narrator (voiced by Will Stamper) telling the adventures of the hundreds of friends aboard the S.S. Friendship, as well as Hatty Hattington, who is known as "best friend to one and all"."""

    key = list(string.ascii_uppercase)
    random.shuffle(key)
    _test_simplesubstitution(
        plaintext,
        score_functions=[english_scorer.quadgrams()],
        key=key
    )


def test_500_character_text():
    """Testing text of length ~500"""
    plaintext = """Upon its release, the novel received near universal acclaim. Although Dickens' contemporary Thomas Carlyle referred to it disparagingly as that "Pip nonsense," he nevertheless reacted to each fresh instalment with "roars of laughter."Later, George Bernard Shaw praised the novel, as "All of one piece and consistently truthful." During the serial publication, Dickens was pleased with public response to Great Expectations and its sales; when the plot first formed in his mind, he called it "a very fine, new and grotesque idea."""

    key = list(string.ascii_uppercase)
    random.shuffle(key)
    _test_simplesubstitution(
        plaintext.upper(),
        score_functions=[english_scorer.quadgrams()],
        key=key
    )
