#!/usr/bin/env python3

from lantern.modules import shift

from typing import Iterable


def shift_encrypt(key: int, byte: int) -> int:
    return (byte + key) % 255


def shift_decrypt(key: int, byte: int):
    return (byte - key) % 255


def header_matcher(value: Iterable) -> int:
    return 0 if value[:8] == [137, 80, 78, 71, 13, 10, 26, 10] else -1


with open("example.png", "rb") as image:
    image_bytes = bytearray(image.read())

KEY = 144
encrypted_bytes = shift.encrypt(KEY, image_bytes, shift_encrypt)

print(f"Encrypted header: {encrypted_bytes[:8]}")

# Decrypt the image by finding a matching PNG header
decryptions = shift.crack(
    encrypted_bytes, header_matcher, min_key=0, max_key=255, shift_function=shift_decrypt
)

print(f"Decrypted Header: {decryptions[0].plaintext[:8]}")
