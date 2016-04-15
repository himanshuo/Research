import traceback
import sqlite3
import nltk
import os
import json
import time
import operator
import random
import math
import sys
import time
from collections import OrderedDict
from constant import *


input_database = 'second.db'
read_conn = sqlite3.connect(input_database)
write_conn = sqlite3.connect(input_database)
db_read = read_conn.cursor()
db_write = write_conn.cursor()
db_read.execute("delete from FullVector;")
tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
tweets = db_read.execute("SELECT * from Tweet")
temp_tweets = []



def get_pos_features(tagger):
    out = [0 for i in range(0,len(POS_INDEX))]

    for t in tagger:
        try:
            index = POS_INDEX[t[1].upper()]
            out[index] += 1
            if t[1].upper() in ['NN', 'NNS', 'NNP', 'NNPS']:
                out[POS_INDEX['NOUN']] += 1
            elif t[1].upper() in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                out[POS_INDEX['VERB']] += 1
            elif t[1].upper() in ['JJ', 'JJR', 'JJS']:
                out[POS_INDEX['ADJECTIVE']] += 1
            elif t[1].upper() in ['PRP', 'PRP$', 'WP','WP$']:
                out[POS_INDEX['PRONOUN']] += 1
            elif t[1].upper() in ['RB', 'RBR', 'RBS', 'WRB']:
                out[POS_INDEX['ADVERB']] += 1
        except:
            print('not adding {} because punctuation'.format(t[1]))
    out = str(out)[1:-1]
    return out

CHUNK_SIZE = 1000
def process_chunk(tweets):
    process_list = []
    tweets_map = OrderedDict()
    i = 0
    # temp_map = {} # id->pos_tag vector
    print(len(tweets))
    for item in tweets:
        i += 1
        # print "inside: " + str(i)
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
                new_tokens.append(token.lower())
        if len(new_tokens) > 10 and len(new_tokens) < 39:  # check to see why 8873 is never rwritten?
            tweets_map[item[0]] = len(new_tokens)
            process_list = process_list + new_tokens

    print("starting nltk stuff")
    start = time.time() # 134.500674009
    i = 0
    tagged1 = nltk.pos_tag(process_list)
    print("done with nltk stuff")
    for x in tweets_map.keys():
        # print x
        length = tweets_map[x]
        tagged = tagged1[:length]
        tagged1 = tagged1[length:]
        pos_features = get_pos_features(tagged)
        # print('\n ')
        # print(tagged)
        # print(pos_features)
        # print(' \n')
        db_read.execute("insert into FullVector(tweet_id, full_vector) values (?, ?);", [x, pos_features])

        # if str(tagged) != str(temp_map[x]):
        #     print('bad')
        #     # print x
            # print(tagged)
            # print(temp_map[x])


    read_conn.commit()

    end = time.time()

    # for item in db_read.execute("select * from FullVector limit 20"):
    #     print(item)
    print("IT TOOK {} seconds".format(end-start))

for item in tweets:
    temp_tweets.append(item)
for i in range(0,int(len(temp_tweets)/CHUNK_SIZE)):
    process_chunk(temp_tweets[:CHUNK_SIZE])
    temp_tweets = temp_tweets[CHUNK_SIZE:]
    print("{} chunks processed".format(i))
process_chunk(temp_tweets)
