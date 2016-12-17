from cckrypto.NgramScore import NgramScore
from cckrypto import Caesar

fitness = None

def setup_module(module):
    global fitness
    fitness = NgramScore('cckrypto/english_quadgrams.txt')

def test_quick_brown_fox():
    ciphertext = "QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD"
    plaintext = Caesar.crack(ciphertext, fitness)
    assert plaintext == "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
