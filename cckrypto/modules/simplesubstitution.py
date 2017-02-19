from pycipher import SimpleSubstitution
import random
import re
import math

def crack(ciphertext, fitness):
    max_key = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    max_score = -math.inf
    parent_score, parent_key = max_score, max_key
  
    iteration = 0
    unicity = 500
    while iteration < unicity:
        iteration += 1

        random.shuffle(parent_key)
        plaintext = SimpleSubstitution(parent_key).decipher(ciphertext)
        parent_score = fitness.score(plaintext)

        # Find local maximum
        step = 0
        while step < 100:
            a = random.randint(0, 25)
            b = random.randint(0, 25)

            child_key = parent_key

            # Swap two characters in the child
            child_key[a], child_key[b] = child_key[b], child_key[a]
            plaintext = SimpleSubstitution(child_key).decipher(ciphertext)
            score = fitness.score(plaintext)

            # if the child was better, replace the parent with it
            if score > parent_score:
                parent_score = score
                parent_key = child_key
                step = 0
            step += 1

        # keep track of best score seen so far
        if parent_score > max_score:
            max_score, max_key = parent_score, parent_key
            print("Best score " + str(max_score))
            print("decrypt " + SimpleSubstitution(max_key).decipher(ciphertext, True))

    return SimpleSubstitution(max_key).decipher(ciphertext, True)
