import sqlite3
import nltk
import os
import json
import time
import operator
import random
import math
import sys
import functions
from TwitterSearch import *
from constants import *

tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
keys = [ts1,ts2,ts3,ts4,ts5,ts6,ts7,ts8,ts9,ts10]

conn = sqlite3.connect('second.db')
cursor = conn.cursor()

def tags_from_txt(txt):
    """
    tweet text -> [hashtags in tweet]
    """
    try:
        txt = str(txt)
        hashs = []
        data = tokenizer.tokenize(txt)
        for i in range(len(data)):
            if data[i] == "#" and i+1 <len(data):
                hashs.append(data[i+1])
        return hashs
    except:
        return []

# todo: remove conn, c
# todo: rename hashs
# todo: counter to num_seen
# todo: upsert
# todo: hashs.items()
def add_new_tags_to_db(branching_tags):
    """
        branching_tags: {hashtag : num_references}
        if new tag, then add to db
        else modify db to reflect that this dict of hashtags has been seen more times
    """
    print branching_tags

    for hashtag, ref in branching_tags.items():
        hashtag = hashtag.lower()

        num_seen = 0
        for i in cursor.execute("SELECT * FROM Hashtag WHERE hashtag = ?",(str(hashtag),)):
            num_seen += i[3]

        if num_seen == 0:
            # query = "INSERT INTO Hashtag (hashtag,checked,ref) VALUES(?,0," + str(hashs[item]) + ")",(item,)
            query = "INSERT INTO Hashtag (hashtag,checked,ref) VALUES(\"{}\",0,0)".format(hashtag)
        else:
            # query = "UPDATE Hashtag SET ref = " + str(counter + hashs[item]) + " WHERE hashtag==\"" + item + "\""
            query = "UPDATE Hashtag SET ref = {} WHERE hashtag={}".format(num_seen+ref, hashtag)


        cursor.execute(query)
        conn.commit()

def get_content_words(tokens):
    """
        filtering of tweet words.
        Takes in a tweet and removes all 'bad' words
    """
    hashtag = False
    hashtag2 = False
    new_tokens = []
    for token in tokens:
        if token == "@" or token == "#":
            hashtag = True
        elif token == "https" or token == "http" or token == "..http" or token == "..https":
            hashtag2 = True
        elif hashtag2 == True:
            hashtag2 = False
            hashtag = True
        elif hashtag:
            hashtag = False
        else:
            if token.lower() not in stopwords and token not in punctuations:
                new_tokens.append(token.lower()) # EVERYTHING IS LOWER CASE
    return new_tokens

# def get_content_words(tokens):
#     """
#         filtering of tweet words.
#         Takes in a tweet and removes all 'bad' words
#     """
#     invalid_words = ["https", "http", "..http", "..https"]
#     tokens = [token for token in tokens if token not in invalid_words]
#
#     hashtag_indicator = ["@", "#"]
#     is_hashtag = False
#     new_tokens = []
#
#     for token in tokens:
#         if token in hashtag_indicator:
#             is_hashtag = True
#         elif is_hashtag:
#             is_hashtag = False
#         else:
#             if token.lower() not in stopwords and token not in punctuations:
#                 new_tokens += token # EVERYTHING IS LOWER CASE
#     return new_tokens

def mark_tag_as_checked(hashtag):
    # mark checked
    cursor.execute("UPDATE Hashtag SET checked = 1 WHERE hashtag==\"" + hashtag +"\"")
    conn.commit()

def contains_key(mydict, mykey):
    try:
        mydict[mykey]
        return True
    except:
        return False

def is_new_tweet(tweet):
    """
        returns True if db does not contain this tweet already
    """
    counting = 0
    # todo: turn this into a count query
    # todo: change counting to num_seen
    for i in cursor.execute("select * from Tweet where text == ?",(tweet['retweeted_status']['text'],)):
        counting += 1
    return counting == 0




def meets_content_threshold(tweet):
    # assures no bad characters here as well
    try:
        text = str(tweet['retweeted_status']['text'])
    except:
        return False
    tokens = tokenizer.tokenize(text)
    new_tokens = get_content_words(tokens)
    return len(new_tokens) > content_threshold


def filter_tweets(tweets):
    out = []

    for tweet in tweets:
        if tweet['retweet_count'] > retweet_count_threshold and \
            contains_key(tweet, 'retweeted_status') and \
            is_new_tweet(tweet) and \
            tweet['retweeted_status']['user']['followers_count'] > follower_count_threshold and \
            meets_content_threshold(tweet):
                out.append(tweet)
    return out


def upsert_user(username_id, username_name, username_followers):
    # todo: there is probably a sqlite upsert function

    # num times user has been seen.
    count = 1
    for i in cursor.execute("SELECT * from Username WHERE userid==" + str(username_id) + ";"):
        count += i[4]

    if count == 1:
        # add user if doesnt already exist
        cursor.execute("INSERT INTO Username Values(" + username_id + "," + username_followers + ",\"" + username_name + "\",0,1);")
        conn.commit()
    else:
        # update that we saw this user once more
        cursor.execute("UPDATE Username SET ref = " + str(count) + " WHERE userid==" + str(username_id) + ";")
        conn.commit()


def add_tweets_to_db(tweets):
    for tweet in tweets:
        # add each tweet to db.
        # this will likely break for whatever reasons.
        # ignore tweets that break
        try:
            add_tweet_to_db(tweet)
        except:
            print("failed to add: {}".format(str(tweet)))

def create_branching_tags(tweet):
    # branching_tags: {hashtags: ref}
    branching_tags = {}

    # if exists in branching tags, then increment counter, else add to branching tags with ref=1
    scraped = tags_from_txt(tweet['retweeted_status']['text'])
    for item in scraped:
        try:
            branching_tags[item.lower()] += 1
        except:
            branching_tags[item.lower()] = 1

    return branching_tags

def add_tweet_to_db(tweet):
    """
        adds tweets, associated users, associated hashtags to db
    """
    # get database stuff
    username_name = str(tweet['retweeted_status']['user']['screen_name'])
    username_id = str(tweet['retweeted_status']['user']['id'])
    username_followers = str(tweet['retweeted_status']['user']['followers_count'])
    tweet_text = str(tweet['retweeted_status']['text'])
    tweet_retweets = str(tweet['retweeted_status']['retweet_count'])
    tweet_favorites = str(tweet['retweeted_status']['favorite_count'])
    tweet_twitterid = str(tweet['retweeted_status']['id'])

    #add associate user
    upsert_user(username_id, username_name, username_followers)
    # add tweet into db
    cursor.execute("INSERT INTO Tweet (username,text,retweet_count,favorite_count,twitterID) Values(" + username_id + ",?," + tweet_retweets + "," + tweet_favorites + "," + tweet_twitterid + ")",(tweet_text,))
    conn.commit()

    # add hashtags to db
    branching_tags = create_branching_tags(tweet)
    add_new_tags_to_db(branching_tags)


def tag_query(active_tags):
    global keys
    tweets = []
    for tag in active_tags:
        # scrape every 5 seconds
        time.sleep(5)
        # build hashtag in proper format
        hashtag = "#" + str(tag)


        try:
            # get data from twitter using api
            tso = TwitterSearchOrder()
            tso.set_keywords([hashtag]) # AND matching for keywords in list
            tso.set_language('en')
            tso.set_include_entities(False)
            ts = keys[0]
            tweets = ts.search_tweets_iterable(tso)
            # mark hashtag as checked
            mark_tag_as_checked(hashtag)
        except Exception as e:
            # if fail, move key[0] to end and sleep to allow key to reset
            keys = keys[1:] + [keys[0]]
            time.sleep(10)
    return tweets

def user_query(active_users):
    tweets = []
    for user in active_users:
        user = str(user[2])
        try:
            tuo = TwitterUserOrder(user)
            # todo: search_tweets_iterable gets all historical tweets of user in chunks. Perhaps stop getting more chunks if x condition
            tweets += ts.search_tweets_iterable(tuo)
        except Exception as e:
            # if fail, move key[0] to end and sleep to allow key to reset
            keys = keys[1:] + [keys[0]]
            time.sleep(10)
    return tweets


def scrape_by_tag():
    # determine which tags to look for. tags that havent already been checked, order by decreaseing number of references to them
    active_tags = cursor.execute("SELECT * from Hashtag where checked == 0 ORDER BY ref DESC limit 1")
    time.sleep(5)
    active_tag_strings = [ str(tag[1]) for tag in active_tags]
    tweets = tag_query(active_tag_strings)
    tweets = filter_tweets(tweets)
    add_tweets_to_db(tweets)



def scrape_by_user():
    active_users = cursor.execute("SELECT * from Username WHERE checked == 0 limit 1")
    tweets = user_query(active_users)
    tweets = filter_tweets(tweets)
    add_tweets_to_db(tweets)

def init():
    for data in cursor.execute("SELECT count(*) FROM Hashtag"):
        if data[0] == 0: # no initial hashtags
            for hashtag in ["trump", "donuld","americanpolitics"]:
                query = "INSERT INTO Hashtag (hashtag,checked,ref) VALUES('{}',0,0)".format(hashtag)
                cursor.execute(query)
                conn.commit()


    # for data in cursor.execute("SELECT count(*) FROM User"):
    #     if data[0] == 0: # no initial hashtags


# MAIN
if __name__=="__main__":
    init()
    while True:
        scrape_by_tag()
        scrape_by_user()
