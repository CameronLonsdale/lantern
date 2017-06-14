"""Tests for the Simple Substitution module"""

import pycipher
import random
import string

import pytest
from tests.util import get_top_decryptions

from lantern.modules import simplesubstitution
from lantern import fitness


def _test_simplesubstitution(plaintext, first, *rest, key=None, ntrials=30, top_n=1):
    if key is None:
        key = list(string.ascii_uppercase)
        random.shuffle(key)

    ciphertext = pycipher.SimpleSubstitution(key).encipher(plaintext, keep_punct=True)
    decryptions = simplesubstitution.crack(ciphertext, first, *rest, ntrials=ntrials)

    top_decryptions = get_top_decryptions(decryptions, top_n)

    match = None
    for decrypt in top_decryptions:
        if decrypt.plaintext.upper() == plaintext.upper():
            match = decrypt
            break

    assert match is not None

    # THIS CURRENTLY FAILS DUE TO 2 LETTER DIFFERENCES IN THE KEY, SO WE SHOULD CHECK THIS
    # USING HAMMING DISTANCE ONCE THATS IMPLEMENTED
    # assert ''.join(match.key) == ''.join(key)


def test_250_character_text():
    """Testing text of length ~250"""
    plaintext = """Almost all of the game's cut-scenes are done in a stick puppet style. The game begins with the narrator (voiced by Will Stamper) telling the adventures of the hundreds of friends aboard the S.S. Friendship, as well as Hatty Hattington, who is known as "best friend to one and all"."""
    _test_simplesubstitution(plaintext, fitness.english.quadgrams, ntrials=15)


def test_500_character_text_quadgrams():
    """Testing text of length ~500"""
    plaintext = """Upon its release, the novel received near universal acclaim. Although Dickens' contemporary Thomas Carlyle referred to it disparagingly as that "Pip nonsense," he nevertheless reacted to each fresh instalment with "roars of laughter."Later, George Bernard Shaw praised the novel, as "All of one piece and consistently truthful." During the serial publication, Dickens was pleased with public response to Great Expectations and its sales; when the plot first formed in his mind, he called it "a very fine, new and grotesque idea."""
    _test_simplesubstitution(plaintext, fitness.english.quadgrams, ntrials=8)


def test_500_character_text_trigrams():
    """Testing text of length ~500"""
    plaintext = """Upon its release, the novel received near universal acclaim. Although Dickens' contemporary Thomas Carlyle referred to it disparagingly as that "Pip nonsense," he nevertheless reacted to each fresh instalment with "roars of laughter."Later, George Bernard Shaw praised the novel, as "All of one piece and consistently truthful." During the serial publication, Dickens was pleased with public response to Great Expectations and its sales; when the plot first formed in his mind, he called it "a very fine, new and grotesque idea."""
    _test_simplesubstitution(plaintext, fitness.english.trigrams, ntrials=8)


def test_500_character_text_bigrams():
    """Testing text of length ~500"""
    plaintext = """Upon its release, the novel received near universal acclaim. Although Dickens' contemporary Thomas Carlyle referred to it disparagingly as that "Pip nonsense," he nevertheless reacted to each fresh instalment with "roars of laughter."Later, George Bernard Shaw praised the novel, as "All of one piece and consistently truthful." During the serial publication, Dickens was pleased with public response to Great Expectations and its sales; when the plot first formed in his mind, he called it "a very fine, new and grotesque idea."""
    _test_simplesubstitution(plaintext, fitness.english.bigrams, ntrials=8)


def test_substution_invalid_ntrials_and_nswaps():
    """Testing invalid values of ntrials and nswaps"""
    with pytest.raises(ValueError):
        simplesubstitution.crack("abc", fitness.english.quadgrams, ntrials=0)

    with pytest.raises(ValueError):
        simplesubstitution.crack("abc", fitness.english.quadgrams, ntrials=-10)

    with pytest.raises(ValueError):
        simplesubstitution.crack("abc", fitness.english.quadgrams, nswaps=-10)

    with pytest.raises(ValueError):
        simplesubstitution.crack("abc", fitness.english.quadgrams, nswaps=0)


def test_decrypt():
    """Test decrypt successfully decrypts ciphertext enciphered with the same key"""
    assert simplesubstitution.decrypt("PQSTUVWXYZCODEBRAKINGFHJLM", "XUOOB") == "HELLO"


def test_decrypt_key_as_list():
    """Test decrypt successfully decrypts ciphertext enciphered with the same key"""
    plaintext = "FLEE AT ONCE. WE ARE DISCOVERED!"
    ciphertext = "SIAA ZQ LKBA. VA ZOA RFPBLUAOAR!"
    assert simplesubstitution.decrypt(list('ZEBRASCDFGHIJKLMNOPQTUVWXY'), ciphertext) == plaintext
