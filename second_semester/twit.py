import sqlite3
import nltk
import os
import json
import time
import operator
import random
import math
import sys
import unigrammodel
from constant import *

input_database = 'second_first10000.db'

stopwords = unigram_stopwords

tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
threshold = unigram_threshold
conn = sqlite3.connect(input_database)
c = conn.cursor()

stopwords = [u'i',u'to',u'the',u'a',u'and',u'in',u'you',u'my',u'of',u'it',u'for',u'is',u'on',u'that',u'this',u'me'] #under 3

data = []
linked = {}
tweets = c.execute("SELECT * from Tweet")
i = 0
for item in tweets:
    tokens = tokenizer.tokenize(item[2])
    hashtag = False
    hashtag2 = False
    new_tokens = []
    for token in tokens:
        if token == "@" or token == "#":
            hashtag = True
        elif token == "https" or token == "http":
            hashtag2 = True
        elif hashtag2 == True:
            hashtag2 = False
            hashtag = True
        elif hashtag:
            hashtag = False
        else:
            if not token in stopwords:
                new_tokens.append(token.lower())
    if len(new_tokens) > 10 and len(new_tokens) < 39: # check to see why 8873 is never rwritten?
        data.append((new_tokens,item[0]))
        linked[item[0]] = new_tokens
UG = unigrammodel.UnigramModel([x[0] for x in data],stopwords)
print "done"

hashtag_dict = {}
tweets = c.execute("SELECT * from Tweet")
for item in tweets:
    tokens = tokenizer.tokenize(item[2])
    hashtag = False
    for token in tokens:
        if token == "#":
            hashtag = True
        elif hashtag:
            try:
                hashtag_dict[token].append(item[0])
            except:
                hashtag_dict[token] = [item[0]]
            hashtag = False

print "done with the hashtaggin"

def analyze(tweets):
    f = open("similarities.txt","a")
    g = open("similarities_fully.txt","a")
    for i in range(0,len(tweets)):
        for j in range(i+1,len(tweets)):
            try:
                # a is the similarity 0 -> 1 0 is not similar, 1 is very similar (identical)
                # want to have files for .3 to .4 etc..
                # also want to print out the full text instead of just the tokens 
                a = UG.get_similarity(linked[tweets[i]],linked[tweets[j]])
                if a > 0.28 and a < .99:
                    f.write(str(tweets[i]))
                    f.write(",")
                    f.write(str(tweets[j]))
                    f.write(",")
                    f.write(str(a))
                    f.write("\n")

                    g.write(str(linked[tweets[i]]))
                    g.write(",")
                    g.write(str(linked[tweets[j]]))
                    g.write(",")
                    g.write(str(a))
                    g.write("\n")

                    print str(linked[tweets[i]])
                    print str(linked[tweets[j]])
                    print str(a)
                    print " "
            except:
                    print "key error"

    f.close()
    g.close()

ids = [x[1] for x in data]
tags = hashtag_dict
print "tags: "
print tags

dels = []
for item in tags:
    if len(tags[item]) < 2:
        dels.append(item)
for item in dels:
    del tags[item]
i = 3
while i < 100000:
    dels = []
    for item in tags:
        if len(tags[item]) < i:
            analyze(tags[item])
            dels.append(item)
    for item in dels:
        del tags[item]
    i += 1
