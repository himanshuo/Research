import traceback
import sqlite3
import datetime
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

#feature: [bag_of_words0,bag_of_words1,...bag_of_wordsn,  ]



input_database = 'second.db'

stopwords = unigram_stopwords

tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
threshold = unigram_threshold
conn = sqlite3.connect(input_database)
c = conn.cursor()

stopwords = [u'i', u'to', u'the', u'a', u'and', u'in', u'you', u'my',
             u'of', u'it', u'for', u'is', u'on', u'that', u'this', u'me']  # under 3
users = {}
data = []
linked = {}
times = {}
followers = {}
hashtags =[]
for h in c.execute("select hashtag from hashtag"):
    hashtags.append(h[0])

hashtagmap = {} # id -> vector of all hashtags that it has(as feature vector)
usersmap = {}
all_users = []
us = c.execute("SELECT * from Username")
for item in us:
    users[item[2]] = item[1]
    all_users.append(item[2])
all_users = set(all_users)
tweets = c.execute("SELECT * from Tweet limit 1")
i = 0
for item in tweets:
    print item
    times[item[0]] = float(item[6])
    followers[item[0]] = float(users[item[1]])
    tokens = tokenizer.tokenize(item[2])
    hashtag = False
    hashtag2 = False
    temp_tags = []
    temp_users = []
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
            if token in hashtags:
                temp_tags.append(token)
            if token in all_users:  # WHAT IF HASHTAG AND USER ARE SAME -- todo
                temp_users.append(token)
        else:
            if not token in stopwords:
                new_tokens.append(token.lower())
    if len(new_tokens) > 10 and len(new_tokens) < 39:  # check to see why 8873 is never rwritten?
        data.append((new_tokens, item[0]))
        linked[item[0]] = new_tokens
        temp = list(hashtags)
        for x in range(0,len(temp)): # THIS MAY BE MORE efficieNT doing appends of 1 , 0 instead of deep copying every time -- todo
            if temp[x] in temp_tags:
                temp[x] = 1
            else:
                temp[x] = 0
        hashtagmap[item[0]] = temp
        temp = list(all_users)
        for x in range(0,len(temp)):
            if temp[x] in temp_users:
                temp[x] = 1
            else:
                temp[x] = 0
        usersmap[item[0]] = temp

UG = unigrammodel.UnigramModel([x[0] for x in data], stopwords)
print "done"


hashtag_dict = {}
tweets = c.execute("SELECT * from Tweet limit 100")
for item in tweets:
    print item
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

print "done with the hashtagging"


num_results = 0


def similar_time(tweet_id_a, tweet_id_b):
    threshold = 60 * 60 * 24 * tweet_time_difference_threshold
    return abs(times[tweet_id_b] - times[tweet_id_a]) < threshold


def similar_followers(tweet_id_a, tweet_id_b):
    return followers[tweet_id_a] / followers[tweet_id_b] < tweet_follower_difference_threshold and followers[tweet_id_b] / followers[tweet_id_a] < tweet_follower_difference_threshold


def is_asking_retweet(tweet_tokens):
    check_for = ['rt', 'retweet']
    for token in tweet_tokens:
        if 'retweet' in token:
            return True
        if ".rt" in token or 'rt.' in token or ' rt' in token or 'rt' == token:
            return True
        return False

def get_pos(tweet_id):
    print("getpos")
    for v in c.execute("SELECT full_vector from FullVector where tweet_id = ? limit 1", (tweet_id,)):
        return v[0].split(', ')

def get_time_of_day_vect(tweet_id):
    print('time of day')

    for t in c.execute("select created_at from Tweet where tweetid = ? limit 1 ;", (tweet_id,)):
        seconds_since_epoch = float(t[0])
        d = datetime.datetime.fromtimestamp(int(seconds_since_epoch))
        arr = [0,0,0,0,0,0] # [0-3, 4-7, 8-11, 12-15, 16-20, 21-24]
        arr[int(d.hour/4)] = 1
        print(d)
        print(arr)
        return arr

def get_result_popularity(tweet_id_a, tweet_id_b):
    retweet_count_a = 0
    for r in c.execute("select retweet_count from Tweet where tweetid = ?", (tweet_id_a,)):
        retweet_count_a = r[0]

    retweet_count_b = 0
    for r in c.execute("select retweet_count from Tweet where tweetid = ?", (tweet_id_b,)):
        retweet_count_b = r[0]

    print(retweet_count_a)
    print(retweet_count_b)

    if retweet_count_a > retweet_count_b:
        print(1)
        return 1
    else:
        print(0)
        return 0

def analyze(tweets):
    """
    linked: id -> [token]   ([token] is 1 tweet)
    tweets: [id]
    """
    global num_results
    f = open("similarities.txt", "a")
    g = open("similarities_fully.txt", "a")
    for i in range(0, len(tweets)):
        for j in range(i + 1, len(tweets)):

            try:
                # a is the similarity 0 -> 1 0 is not similar, 1 is very similar (identical)
                # want to have files for .3 to .4 etc..
                # also want to print out the full text instead of just the
                # tokens

                a = UG.get_similarity(linked[tweets[i]], linked[tweets[j]])
                if a > 0.28 and a < .99 and similar_time(tweets[i], tweets[j]) and similar_followers(tweets[i], tweets[j]) and not is_asking_retweet(linked[tweets[i]]) and not is_asking_retweet(linked[tweets[j]]):
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

                    # print str(linked[tweets[i]])
                    # print str(linked[tweets[j]])
                    # print str(a)
                    num_results = num_results + 1
                    print(num_results)

                    featurea = UG.get_vector_list(linked[tweets[i]])
                    featureb = UG.get_vector_list(linked[tweets[j]])
                    featurea = featurea + list(hashtagmap[tweets[i]])
                    featureb = featureb + list(hashtagmap[tweets[j]])
                    featurea = featurea + list(usersmap[tweets[i]])
                    featureb = featureb + list(usersmap[tweets[j]])
                    featurea = featurea + [len(linked[tweets[i]])]
                    featureb = featureb + [len(linked[tweets[j]])]
                    featurea = featurea + get_pos(tweets[i])
                    featureb = featureb + get_pos(tweets[j])
                    featurea = featurea + get_time_of_day_vect(tweets[i])
                    featureb = featureb + get_time_of_day_vect(tweets[j])

                    final_feature = []
                    print len(featurea)
                    print len(featureb)
                    print "\n\n\n\n"
                    for i in range(0,len(featurea)):
                        final_feature.append(int(featurea[i]) - int(featureb[i]))

                    results = get_result_popularity(tweets[i], tweets[j])




            except Exception as e:
                    traceback.print_exc()

    f.close()
    g.close()

ids = [x[1] for x in data]
tags = hashtag_dict

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
