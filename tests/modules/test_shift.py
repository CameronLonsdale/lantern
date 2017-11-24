"""Tests for the Caeser module"""

import pycipher
import string

import pytest
from tests.util import get_top_decryptions

from lantern.modules import shift
from lantern import fitness


def _test_shift(plaintext, *fitness_functions, key=3, top_n=1):
    ciphertext = pycipher.Caesar(key).encipher(plaintext, keep_punct=True)
    decryptions = shift.crack(ciphertext, *fitness_functions)

    top_decryptions = get_top_decryptions(decryptions, top_n)

    match = None
    for decrypt in top_decryptions:
        if ''.join(decrypt.plaintext).upper() == ''.join(plaintext).upper():
            match = decrypt
            break

    assert match is not None
    assert match.key == key


def test_quick_brown_fox_unigrams():
    """Testing quick brown fox"""
    plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog"
    _test_shift(plaintext, fitness.english.unigrams)


def test_quick_brown_fox_bigrams():
    """Testing quick brown fox with bigrams"""
    plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog"
    _test_shift(plaintext, fitness.english.bigrams)


def test_quick_brown_fox_trigrams():
    """Testing quick brown fox with trigrams"""
    plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog"
    _test_shift(plaintext, fitness.english.trigrams)


def test_quick_brown_fox_quadgrams():
    """Testing quick brown fox with quadgrams"""
    plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog"
    _test_shift(plaintext, fitness.english.quadgrams)


def test_quick_brown_fox_multiple_functions():
    """Testing quick brown fox with multiple fitness functions"""
    plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog"
    _test_shift(plaintext, fitness.english.bigrams, fitness.english.trigrams)


def test_quick_brown_fox_upper():
    """Testing quick brown fox uppercase letters"""
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    _test_shift(plaintext, fitness.english.quadgrams)


def test_quick_brown_fox_patristocrats():
    """Testing quick brown fox broken into groups of 5"""
    plaintext = "TheQu ckBro wnFox Jumps OverT heLaz yDog"
    _test_shift(plaintext, fitness.english.quadgrams)


def test_quick_brown_fox_no_whitespace():
    """Testing quick brown fox no whitespace"""
    plaintext = "thequickbrownfoxjumpsoverthelazydog"
    _test_shift(plaintext, fitness.english.quadgrams)


def test_quick_brown_fox_no_whitespace_upper():
    """Testing quick brown fox no whitespace and uppercase"""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    _test_shift(plaintext, fitness.english.quadgrams)


def test_buzz_buzz_buzz_quadgrams():
    """
    Testing buzz buzz buzz in top 2 results.

    haff haff haff beats it because it has a better freqency distribution.
    """
    plaintext = "BUZZ BUZZ BUZZ"
    _test_shift(plaintext, fitness.english.quadgrams, top_n=2)


def test_narrow_key_range():
    """Test narrower keyrange lowers the amount of brute forcing done"""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    ciphertext = pycipher.Caesar(3).encipher(plaintext, keep_punct=True)

    decryptions = shift.crack(ciphertext, fitness.english.quadgrams, min_key=3, max_key=5)
    assert len(decryptions) == 2
    assert ''.join(decryptions[0].plaintext) == plaintext


def test_invalid_key_range():
    """Test an invalid key throws ValueError"""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    ciphertext = pycipher.Caesar(3).encipher(plaintext, keep_punct=True)

    with pytest.raises(ValueError):
        shift.crack(ciphertext, fitness.english.quadgrams, min_key=7, max_key=2)


def test_decrypt():
    """Test decrypt successfully decrypts ciphertext enciphered with the same key"""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    key = 3
    ciphertext = pycipher.Caesar(key).encipher(plaintext, keep_punct=True)
    assert ''.join(shift.decrypt(key, ciphertext)) == plaintext


def test_decrypt_large_key_wrapped():
    """Test key value is wrapped around by the length of the alphabet"""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    key = 30
    ciphertext = pycipher.Caesar(key).encipher(plaintext, keep_punct=True)
    assert ''.join(shift.decrypt(key, ciphertext)) == plaintext


def test_shifted_punctuation():
    """Test punctuation shifting can be cracked"""
    ciphertext = 'IODJ~Lw*v|Wkh|Uhpla|ri|Dgglwlrq"'
    shift_function = shift.make_shift_function([string.ascii_uppercase, string.ascii_lowercase, string.punctuation])
    top_decryption = shift.crack(ciphertext, fitness.english.quadgrams, shift_function=shift_function)[0]
    assert ''.join(top_decryption.plaintext) == "FLAG{It's_The_Remix_of_Addition}"


def test_decrypt_shifted_punctuation():
    """Test punctuation is also shifted"""
    ciphertext = 'IODJ~Lw*v|Wkh|Uhpla|ri|Dgglwlrq"'
    shift_function = shift.make_shift_function([string.ascii_uppercase, string.ascii_lowercase, string.punctuation])
    assert ''.join(shift.decrypt(3, ciphertext, shift_function)) == "FLAG{It's_The_Remix_of_Addition}"


def test_decrypt_shifted_overflow():
    """Test characters overflow into other cases"""
    ciphertext = 'IODJ~Lw*vbWkhbUhpl{bribDgglwlrq!'
    shift_function = shift.make_shift_function([''.join(chr(x) for x in range(32, 127))])
    assert ''.join(shift.decrypt(3, ciphertext, shift_function)) == "FLAG{It's_The_Remix_of_Addition}"


def test_decrypt_byte_shifting():
    """Test bytes can be shifted"""
    def shift_bytes(shift, symbol):
        return symbol + shift

    ciphertext = [0xcf, 0x9e, 0xaf, 0xe0]
    shifted = shift.decrypt(15, ciphertext, shift_bytes)
    assert ''.join(str(hex(c))[2:] for c in shifted) == "deadbeef"


def test_decrypt_list():
    """Test decrypt can handle ciphertext as a list"""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    key = 3
    ciphertext = pycipher.Caesar(key).encipher(plaintext, keep_punct=True)
    assert ''.join(shift.decrypt(key, list(ciphertext))) == plaintext


def test_crack_list():
    """Test crack can handle ciphertext as a list"""
    plaintext = list("THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG")
    _test_shift(plaintext, fitness.english.bigrams, fitness.english.quadgrams)


def test_multi_symbol_decryption():
    """Test a ciphertext which uses multiple characters as a single symbol"""
    ciphertext = ['TF', 'SU']

    # In this (not very good) example, we split the ciphertext into pairs, and the shift function
    # only shifts the second letter. So essentially a shift cipher applied to every second letter
    # We can solve it using this method, or by seperating the shifted letters and decrypting that.
    def shift_function(shift, symbol):
        a, b = symbol[:]
        print(a)
        return a + chr(ord(b) - shift)

    assert ''.join(shift.decrypt(1, ciphertext, shift_function)) == "TEST"
