from __future__ import division
from collections import defaultdict as ddict
import itertools
import math
import random

class NGrams(object):
    """
    compute unsmoothed ngrams
    an unsmoothed ngram is the set of probabilities given to each n-length permutation of the tokens in the input.
    input: some corpus
    tokens: each unique word in the corpus
    permutation: arrangement of tokens
    n-length permutation: all permutations that have length n
    probability of each permutation: the number of times a specific permutation occurs in the corpus / total permutations possible
    ngram: the matrix of permutation to its probability

    Usage:
    ngrams = Ngrams(2,['my', 'words','haha'])
    probs = ngrams.probability()
    """
    def __init__(self, max_n, words=None):
        self._max_n = max_n # n
        self._n_range = range(1, max_n + 1) #[1,2,...n,n+1]
        #_counts is just a dictionary that has a default value of 0 if no value is provided for some key.
        self._counts = ddict(lambda: 0) # {  (w0,w1,w2):1, (ngram_2):4, (ngram_3):0, ... }
        # if words were supplied, update the counts
        if words is not None:
            self.update(words)
    def update(self, words):
        """The result of this function will be adding the counts of ngrams of various lengths to the _counts dict.
         If some ngram already exists in the _counts dict, its value will be increased.
        :param words: a list of words
        :return:
        """

        # increment the total word count, storing this under
        # the empty tuple - storing it this way simplifies
        # the _probability() method
        self._counts[()] += len(words)
        # count ngrams of all the given lengths
        for i, word in enumerate(words): # for each word,
            for n in self._n_range: # for 1,2,3,n,n+1
                if i + n <= len(words): # if the number of words from i to the end is less than n
                    ngram_range = range(i, i + n) # range(start, stop) gives you a generator that just yields vals from start to stop
                    ngram = [words[j] for j in ngram_range] # create a list [word0, word1, word2, ... word]. aka ngram.
                    self._counts[tuple(ngram)] += 1

    def probability(self, words):
        """

        :param words: words to find probability for
        :return:return probability for said group of words.
        """
        if len(words) <= self._max_n:
            return self._probability(words)
        else:
            prob = 1
            for i in range(len(words) - self._max_n + 1):
                ngram = words[i:i + self._max_n]
                prob *= self._probability(ngram)
            return prob

    def _probability(self, ngram):
        # get count of ngram and its prefix
        ngram = tuple(ngram)
        ngram_count = self._counts[ngram]
        prefix_count = self._counts[ngram[:-1]]
        # divide counts (or return 0.0 if not seen)
        if ngram_count and prefix_count:
            return ngram_count / prefix_count
        else:
            return 0.0


def get_probability_for_sentence_from_filename(filename, sentence):
    print('------------------------------- {} ------------------------------- '.format(filename))
    ngrams = NGrams(2,open(filename,'r').read().split())
    print("given '{}', it is {}% likely that the next word is '{}'".format(

        sentence.split()[:-1],
        ngrams.probability(sentence.split()),
        sentence.split()[-1]

        )
    )
    print("'{}' appears {} time(s) in the file.".format(sentence, ngrams._counts[tuple(sentence.split())]))
    print('A few major phrases in the file are:')
    for k,v in ngrams._counts.items():
        if v > 10 and len(k)>1 :
            print('{} : {} has probability {}'.format(k,v, ngrams.probability(k)))


if __name__=="__main__":
    filename = input('filename:')
    sentence = input('sentence:')
    get_probability_for_sentence_from_filename(filename, sentence)
