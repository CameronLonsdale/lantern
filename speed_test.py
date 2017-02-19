import pycipher
import os
import random

from functools import partial

from cckrypto.score_functions import (
    ngram, corpus
)
from cckrypto.modules import caesar

"""Testing the entire bee move script."""
with open(os.path.join('tests', 'beemoviescript.txt')) as bee:
    for line in bee:
        plaintext = line.rstrip().upper()

        if not plaintext:
            continue

        print(plaintext)

        # Encipher line using random Caesar cipher
        cipher = pycipher.Caesar(
            random.randint(caesar.MIN_KEY, caesar.MAX_KEY)
        )
        ciphertext = cipher.encipher(plaintext, keep_punct=True)

        # Use cckrypto to break it
        decryptions = caesar.crack(
            ciphertext,
            score_functions=[
                ngram.quadgram.score,
                partial(corpus.english_words.score, whitespace_hint=True)
            ]
        )
        top_three = decryptions[0:3]
        if not any(plaintext == d[0] for d in top_three):
            print(plaintext)
            print(decryptions)
            # import sys
            # sys.exit()

assert 1 == 2