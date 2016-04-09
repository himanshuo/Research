import sqlite3
import nltk
import os
import json
import time
import operator
import random
import math
import sys
#import functions
from nltk.stem.snowball import EnglishStemmer
from constant import *

class UnigramModel:

    def __init__(self,list_of_documents,stopwords):
        print "started"
        num_docs = len(list_of_documents)
        self.list_of_documents = list_of_documents
        self.doc_freq = {}
        self.stemmer = EnglishStemmer()
        self.punctuations = unigram_punctuations
        self.threshold = 10 # might be too high, too low is too specific
        self.stopwords = stopwords # maybe this or maybe larger list in constants.py
        for doc in list_of_documents:
            for word in set(self.process_document(doc)):
                if word not in stopwords:
                    try:
                        self.doc_freq[word] += 1
                    except:
                        self.doc_freq[word] = 1
        self.idf = {}
        for word in self.doc_freq:
            if self.doc_freq[word] > self.threshold:
                self.idf[word] = 1.0 + math.log((num_docs + 0.0)/(self.doc_freq[word]))
        self.dict_list = self.doc_freq.keys()

    def get_vector_list(self,document):
        vec = self.get_vector(document)
        to_return = list(self.dict_list)
        for x in range(0,len(to_return)):
            try:
                to_return[x] = vec[to_return[x]]
            except:
                to_return[x] = 0
        return to_return

    def process_document(self,doc):
        good_tokens = []
        for token in doc:
            if token in self.punctuations:
                pass
            else:
                good_tokens.append(self.stemmer.stem(token.lower()))
        return good_tokens

    def sublinear_scaled(self,i):
        if i < 1:
            return i
        else:
            return 1.0 + math.log(i)

    def get_vector(self,document):
        vector = {}
        for word in self.process_document(document):
            try:
                vector[word] += 1
            except:
                vector[word] = 1
        dels = []
        for item in vector:
            if item not in self.idf:
                dels.append(item)
        for item in dels:
            del vector[item]
        for item in vector:
            vector[item] = self.idf[item] * self.sublinear_scaled(vector[item])
        return vector

    def magnitude(self,vector):
        count = 0
        for word in vector:
            count += vector[word] ** 2
        return math.sqrt(count)

    def get_similarity(self,doc1, doc2):
        vector1 = self.get_vector(doc1)
        vector2 = self.get_vector(doc2)
        count = 0
        for item in vector1:
            if item in vector2:
                count += vector1[item] * vector2[item]
        try:
            return ((count + 0.0) / self.magnitude(vector1) ) / (self.magnitude(vector2))
        except:
            return 0.0
