"""Utility functions for tests"""


def get_top_decryptions(decryptions, n):
    """Top N decryptions by score, not position"""
    top_decryptions = []
    index = 0
    next_score = 0

    while n > 0 and index <= len(decryptions) - 1:
        if decryptions[index].score < next_score:
            n -= 1

        top_decryptions.append(decryptions[index])
        index += 1

        if index >= len(decryptions):
            break

        next_score = decryptions[index].score

    return top_decryptions
