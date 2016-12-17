from math import log10

class NgramScore():
    def __init__(self, ngramfile, sep=' '):
        """ Load file with ngram counts and calucalte probailities """
        self.ngrams = dict()
        with open(ngramfile) as f:
            for line in f:
                ngram, count = line.split(sep)
                self.ngrams[ngram.upper()] = int(count)

        self.length = len(ngram)
        self.total = sum(self.ngrams.values())

        # Calculate the log probability
        for key in self.ngrams:
            self.ngrams[key] = log10(float(self.ngrams[key]) / self.total)

        self.floor = log10(0.01 / self.total)

    def score(self, text):
        score = 0
        for i in range(len(text) - self.length + 1):
            ngram = text[i: i + self.length]
            if ngram in self.ngrams:
                score += self.ngrams[ngram]
            else:
                # Push bad solutions down
                score += self.floor
        return score
