from collections import defaultdict


def frequency_analyze(text, n=1):
    # TODO: work with different sized ngrams
    frequency = defaultdict(lambda: 0, {})
    for symbol in text:
        frequency[symbol] += 1

    return frequency


def frequency_to_probability(frequency_map, decorator=lambda f: f):
    total = sum(frequency_map.values())
    return {k: decorator(float(v) / total) for k, v in frequency_map.items()}


def index_of_coincidence(text):
    frequency = frequency_analyze(text)
    N = len(text)
    return _calculate_ioc(frequency, N)


def avg_index_of_coincidence(texts):
    average = 0
    for text in texts:
        average += index_of_coincidence(text)
    return average / len(texts)


def chi_squared(source_frequency, target_frequency):
    source_len = sum(source_frequency.values())
    body = lambda n: (source_frequency[n] - source_len * target_frequency[n])**2 / (source_len * target_frequency[n])
    return sum(body(n) for n in source_frequency)


ENGLISH_IC = 0.066


def _calculate_ioc(frequency_map, N):
    coms_of_letters = sum((frequency_map[n] * (frequency_map[n] - 1)) for n in frequency_map)
    return float(coms_of_letters) / (N * (N - 1))
