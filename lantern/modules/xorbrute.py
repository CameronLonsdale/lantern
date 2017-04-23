import logging
import binascii
import string

from .NgramScore import NgramScore
from .util import remove_punctuation


def xor(input_bytes, key):
    output = b''
    for char in input_bytes:
        output += bytes([char ^ key])

    return output


def crack(hex_string, num_bytes, fitness):
    decryptions = list()
    binarray = bytes.fromhex(hex_string)

    for key in range(2**(num_bytes*8)):
        plaintext = ''.join(map(chr, xor(binarray, key)))

        if all(c in string.printable for c in plaintext):
            rank = (plaintext, fitness.score(remove_punctuation(plaintext)))
            decryptions.append(rank)

    # Sort based on best score
    decryptions = sorted(decryptions, key=lambda x: x[1], reverse=True)
    map(logging.debug, decryptions)

    return decryptions
