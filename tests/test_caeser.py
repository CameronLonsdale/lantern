from cckrypto.NgramScore import NgramScore
from cckrypto import Caesar
from cckrypto.util import remove_punctuation
import pycipher
import random
import logging

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

fitness = dict()

def setup_module(module):
    global fitness
    fitness[1] = NgramScore('cckrypto/english_monograms.txt')
    fitness[2] = NgramScore('cckrypto/english_bigrams.txt')
    fitness[3] = NgramScore('cckrypto/english_trigrams.txt')
    fitness[4] = NgramScore('cckrypto/english_quadgrams.txt')
    fitness[5] = NgramScore('cckrypto/english_quintgrams.txt')

def test_quick_brown_fox():
    ciphertext = "QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD"
    plaintext = Caesar.crack(ciphertext, fitness[4])
    assert plaintext == "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"

def test_defend_castle_wall():
    ciphertext = "efgfoe uif fbtu xbmm pg uif dbtumf"
    plaintext = Caesar.crack(ciphertext, fitness[4]).lower()
    assert plaintext == "defend the east wall of the castle"

# Aim for 95% accuracy in decryption with static fitness scoring
def test_entire_bee_movie_quadgrams():
    with open('tests/beemoviescript.txt') as bee:
        lines = filter(None, (line.rstrip() for line in bee))

    num_lines = len(lines)
    incorrect = 0.0
    for plaintext in lines:
        plaintext = plaintext.upper()

        # Encipher line using random Caesar cipher
        cipher = pycipher.Caesar(
            random.randint(Caesar.MIN_KEY, Caesar.MAX_KEY)
        )
        ciphertext = cipher.encipher(plaintext, True)

        # Use cckrypto to break it
        decrypted = Caesar.crack(ciphertext, fitness[4])
        if plaintext != decrypted:
            incorrect += 1
            print("plaintext = " + plaintext)
            print("decrypted = " + decrypted)

    assert incorrect / num_lines <= 0.05

# Aim for 95% accuracy in decryption with dynamic fitness scoring
def test_entire_bee_movie_ngrams():
    with open('tests/beemoviescript.txt') as bee:
        lines = filter(None, (line.rstrip() for line in bee))

    num_lines = len(lines)
    incorrect = 0.0
    for plaintext in lines:
        plaintext = plaintext.upper()

        # Encipher line using random Caesar cipher
        cipher = pycipher.Caesar(
            random.randint(Caesar.MIN_KEY, Caesar.MAX_KEY)
        )
        ciphertext = cipher.encipher(plaintext, True)

        # Choose fitness score based on length of line
        length = clamp(len(remove_punctuation(plaintext)), 1, 5)
        best_fitness = fitness[length]

        # Use cckrypto to break it
        decrypted = Caesar.crack(ciphertext, best_fitness)
        if plaintext != decrypted:
            incorrect += 1
            print("plaintext = " + plaintext)
            print("decrypted = " + decrypted)

    assert incorrect / num_lines <= 0.05
