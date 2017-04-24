import os
from collections import defaultdict

def frequency_analyze(ciphertext):
    frequency = defaultdict(lambda: 0, {})
    for symbol in ciphertext:
        frequency[symbol] += 1

    return frequency


def ioc_calculator(frequency_map, N):
    return float(sum((frequency_map[n] * (frequency_map[n] - 1)) for n in frequency_map)) / (N * (N - 1))


def index_of_coincidence(ciphertext):
    frequency = frequency_analyze(ciphertext)
    N = len(ciphertext)
    return ioc_calculator(frequency, N)


def average_ic(texts):
    average = 0
    for text in texts:
        average += index_of_coincidence(text)
    return average / len(texts)


def chi_squared(source_frequency, target_frequency):
    source_len = sum(source_frequency.values())
    body = lambda n: (source_frequency[n] - source_len * target_frequency[n])**2 / (source_len * target_frequency[n])
    return sum(body(n) for n in source_frequency)

ENGLISH_IC = 0.066

dir_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'english_ngrams'
)

UNIGRAM_FILE = os.path.join(dir_path, 'english_unigrams')

_english_unigram = None


def english_unigram():
    global _english_unigram
    if _english_unigram is None:
        _english_unigram = build_ngram_frequencies(UNIGRAM_FILE)
    return _english_unigram


def build_ngram_frequencies(ngramfile, sep=" "):
    ngrams = {}
    with open(ngramfile) as f:
        for line in f:
            ngram, count = line.split(sep)
            ngrams[ngram.upper()] = int(count)

    length = len(ngram)
    total = sum(ngrams.values())

    # Calculate the log probability
    return {k: (float(v) / total) for k, v in ngrams.items()}
