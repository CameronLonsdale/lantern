"""Tests for the Caser module."""
import pycipher
import random
import os

from cckrypto.score_functions.ngram import quadgram_score
from cckrypto.modules import caesar
from cckrypto.util import remove_punctuation


def test_quick_brown_fox():
    """Testing quick brown fox."""
    ciphertext = "QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD"
    decryptions = caesar.crack(ciphertext, quadgram_score)
    best_decryption = decryptions[0][0].upper()
    assert best_decryption == "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"


def test_defend_castle_wall():
    """Testing defend castle wall."""
    ciphertext = "efgfoe uif fbtu xbmm pg uif dbtumf"
    decryptions = caesar.crack(ciphertext, quadgram_score)
    best_decryption = decryptions[0][0].lower()
    assert best_decryption == "defend the east wall of the castle"


def test_buzz_buzz_buzz():
    """Testing buzz buzz buzz."""
    plaintext = "buzz buzz buzz"
    ciphertext = pycipher.Caesar(3).encipher(plaintext, keep_punct=True)

    decryptions = caesar.crack(ciphertext, quadgram_score)
    best_decryption = decryptions[0][0].lower()
    assert best_decryption == plaintext


# Aim for correct decryption in the top 10 decryptions.
def test_entire_bee_movie_quadgrams():
    """Testing the entire bee move script."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'beemoviescript.txt')) as bee:
        for line in bee:
            plaintext = line.rstrip().upper()
            if len(remove_punctuation(plaintext)) < 4:
                continue

            # Encipher line using random Caesar cipher
            cipher = pycipher.Caesar(
                random.randint(caesar.MIN_KEY, caesar.MAX_KEY)
            )
            ciphertext = cipher.encipher(plaintext, keep_punct=True)

            # Use cckrypto to break it
            decryptions = caesar.crack(ciphertext, quadgram_score)
            top_three = decryptions[0:10]
            assert any(plaintext == d[0] for d in top_three)

# # Aim for 95% accuracy in decryption with dynamic fitness scoring
# def test_entire_bee_movie_ngrams():
#     with open('tests/beemoviescript.txt') as bee:
#         lines = filter(None, (line.rstrip() for line in bee))

#     num_lines = len(lines)
#     incorrect = 0.0
#     for plaintext in lines:
#         plaintext = plaintext.upper()

#         # Encipher line using random Caesar cipher
#         cipher = pycipher.Caesar(
#             random.randint(Caesar.MIN_KEY, Caesar.MAX_KEY)
#         )
#         ciphertext = cipher.encipher(plaintext, True)

#         # Choose fitness score based on length of line
#         length = clamp(len(remove_punctuation(plaintext)), 1, 5)
#         best_fitness = fitness[length]

#         # Use cckrypto to break it
#         decrypted = Caesar.crack(ciphertext, best_fitness)
#         if plaintext != decrypted:
#             incorrect += 1
#             print("plaintext = " + plaintext)
#             print("decrypted = " + decrypted)

#     assert incorrect / num_lines <= 0.05
