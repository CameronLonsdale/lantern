#!/usr/bin/env python3

from lantern.modules import shift
import binascii


def shift_bytes(key: int, byte: int) -> int:
    """Subtract byte by key"""
    return byte - key


ciphertext = [0xed, 0xbc, 0xcd, 0xfe]

KEY = 15
decryption = shift.decrypt(KEY, ciphertext, shift_bytes)
print(binascii.hexlify(bytearray(decryption)))
