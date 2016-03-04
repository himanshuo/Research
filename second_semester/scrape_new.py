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
import datetime

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
    # print branching_tags

    for hashtag, ref in branching_tags.items():
        hashtag = hashtag.lower()
        #import pdb;pdb.set_trace()
        num_seen = 0
        for i in cursor.execute("SELECT * FROM Hashtag WHERE hashtag = ?",(str(hashtag),)):
            num_seen += i[3]


        if num_seen == 0:
            # query = "INSERT INTO Hashtag (hashtag,checked,ref) VALUES(?,0," + str(hashs[item]) + ")",(item,)
            cursor.execute("INSERT INTO Hashtag (hashtag,checked,ref) VALUES(?,0,0)", (hashtag,))

        else:
            # query = "UPDATE Hashtag SET ref = " + str(counter + hashs[item]) + " WHERE hashtag==\"" + item + "\""
            # query = "UPDATE Hashtag SET ref = {} WHERE hashtag=\""+hashtag+"\"".format(num_seen+ref)
            cursor.execute("UPDATE Hashtag SET ref = ? WHERE hashtag=?;", (num_seen+ref, hashtag))

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

def mark_user_as_checked(userid):
    # mark checked
    cursor.execute("UPDATE Username SET checked = 1 WHERE userid==?", (userid,))
    conn.commit()

def mark_word_as_checked(word_id):
    cursor.execute("UPDATE SpecialWord SET checked = 1 WHERE id==?", (word_id,))
    conn.commit()


def contains_key(mydict, mykey):
    try:
        mydict[mykey]
        return True
    except:
        return False

def is_new_tweet(tweet_text):
    """
        returns True if db does not contain this tweet already
    """
    counting = 0
    # todo: turn this into a count query
    # todo: change counting to num_seen
    for i in cursor.execute("select * from Tweet where text == ?",(tweet_text,)):
        counting += 1
    return counting == 0




def meets_content_threshold(tweet_text_with_bad_chars):
    # print(tweet_text_with_bad_chars)
    # fixme: for some reason, we are getting the same tweet constantly from twitter
    # assures no bad characters here as well
    try:
        text = str(tweet_text_with_bad_chars)
        # print(text)
    except:
        return False
    tokens = tokenizer.tokenize(text)
    new_tokens = get_content_words(tokens)
    return len(new_tokens) > content_threshold

def add_special_words(tweet_text):
    tokens = tokenizer.tokenize(tweet_text)
    new_tokens = get_content_words(tokens)
    for token in new_tokens:
        # print(token)
        upsert_word(token)

def upsert_word(word):
    # todo: there is probably a sqlite upsert function

    # num times user has been seen.
    count = 1
    for i in cursor.execute("SELECT * from SpecialWord WHERE word==" + str(word) + ";"):
        count += i[3]

    if count == 1:
        # add word if doesnt already exist
        cursor.execute("INSERT INTO SpecialWord(word,checked,ref) Values(\"" + word + "\",0,1);")
        conn.commit()
    else:
        # update that we saw this word once more
        # cursor.execute("UPDATE SpecialWord SET ref = " + str(count) + " WHERE word==\"" + str(word) + "\";")
        cursor.execute("UPDATE SpecialWord SET ref = ? where word==?", (count, word))
        conn.commit()


def filter_tweets(tweets, is_user):
    out = []

    if is_user:
        for tweet in tweets:
            if tweet['retweet_count'] > retweet_count_threshold and \
                not contains_key(tweet, 'retweeted_status') and \
                is_new_tweet(tweet['text']) and \
                tweet['user']['followers_count'] > follower_count_threshold and \
                meets_content_threshold(tweet['text']):
                    out.append(tweet)
    else:
        for tweet in tweets:
            if tweet['retweet_count'] > retweet_count_threshold and \
                contains_key(tweet, 'retweeted_status') and \
                is_new_tweet(tweet['retweeted_status']['text']) and \
                tweet['retweeted_status']['user']['followers_count'] > follower_count_threshold and \
                meets_content_threshold(tweet['retweeted_status']['text']):
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


def add_tweets_to_db(tweets, from_user_query):
    for tweet in tweets:
        # add each tweet to db.
        # this will likely break for whatever reasons.
        # ignore tweets that break
        try:

            add_tweet_to_db(tweet, from_user_query)
        except:
            print("failed to add: {}".format(str(tweet)))

def create_branching_tags(tweet_text):
    # branching_tags: {hashtags: ref}
    branching_tags = {}

    # if exists in branching tags, then increment counter, else add to branching tags with ref=1
    scraped = tags_from_txt(tweet_text)
    for item in scraped:
        try:
            branching_tags[item.lower()] += 1
        except:
            branching_tags[item.lower()] = 1

    return branching_tags

def add_tweet_to_db(tweet, from_user_query):
    """
        adds tweets, associated users, associated hashtags to db
    """
    # get database stuff
    if not from_user_query:
        username_name = str(tweet['retweeted_status']['user']['screen_name'])
        username_id = str(tweet['retweeted_status']['user']['id'])
        username_followers = str(tweet['retweeted_status']['user']['followers_count'])
        tweet_text = str(tweet['retweeted_status']['text'])
        tweet_retweets = str(tweet['retweeted_status']['retweet_count'])
        tweet_favorites = str(tweet['retweeted_status']['favorite_count'])
        tweet_twitterid = str(tweet['retweeted_status']['id'])
        # tweet_created_at = str(tweet['retweeted_status']['created_at'])
        created_at_datetime = datetime.datetime.strptime(tweet['retweeted_status']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        tweet_created_at = (created_at_datetime-datetime.datetime(1970,1,1)).total_seconds()
    else:
        username_name = str(tweet['user']['screen_name'])
        username_id = str(tweet['user']['id'])
        username_followers = str(tweet['user']['followers_count'])
        tweet_text = str(tweet['text'])
        tweet_retweets = str(tweet['retweet_count'])
        tweet_favorites = str(tweet['favorite_count'])
        tweet_twitterid = str(tweet['id'])
        # tweet_created_at = str(tweet['retweeted_status']['created_at'])
        created_at_datetime = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        tweet_created_at = (created_at_datetime-datetime.datetime(1970,1,1)).total_seconds()

    import pdb;pdb.set_trace()
    
    #add associate user
    upsert_user(username_id, username_name, username_followers)
    # add tweet into db
    cursor.execute("INSERT INTO Tweet (username,text,retweet_count,favorite_count,twitterID,created_at) Values(" + username_id + ",?," + tweet_retweets + "," + tweet_favorites + "," + tweet_twitterid +","+str(tweet_created_at)+")",(tweet_text,))
    conn.commit()

    # add hashtags to db
    branching_tags = create_branching_tags(tweet_text)
    add_new_tags_to_db(branching_tags)

    # add special words to db
    add_special_words(tweet_text)
    print(tweet_text)




def tag_query(active_tags):
    global keys
    tweets = []
    for tag in active_tags:
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
            mark_tag_as_checked(str(tag))
        except Exception as e:
            # if fail, move key[0] to end and sleep to allow key to reset
            print('switching keys')
            keys = keys[1:] + [keys[0]]
            time.sleep(10)
    return tweets


def get_two_week_old_tweet_id():

    two_weeks_ago = (datetime.datetime.now() - datetime.timedelta(days=20))
    epoch = datetime.datetime.utcfromtimestamp(0)
    two_weeks_ago_seconds_since_epoch = (two_weeks_ago - epoch).total_seconds() * 1000.0

    try:
        for i in cursor.execute("SELECT twitterID,created_at from tweet WHERE created_at >= ? order by created_at limit 1", (two_weeks_ago_seconds_since_epoch,)):
            return i[0]
    except:
        return 0

def user_query(active_users):
    global keys
    tweets = []
    for user in active_users:
        user_name = str(user[2])
        try:
            tuo = TwitterUserOrder(user_name)
            tuo.set_since_id(get_two_week_old_tweet_id())
            # todo: search_tweets_iterable gets all historical tweets of user in chunks. Perhaps stop getting more chunks if x condition
            ts = keys[0]
            tweets = ts.search_tweets_iterable(tuo)

            # mark user as checked
            mark_user_as_checked(user[0])
        except Exception as e:
            # if fail, move key[0] to end and sleep to allow key to reset
            print('switching keys')
            keys = keys[1:] + [keys[0]]
            time.sleep(10)
    return tweets

# def is_query_empty(db_cursor):
#     print(db_cursor.rowcount)
#     return db_cursor.rowcount <= 0

def scrape_by_tag():
    # determine which tags to look for. tags that havent already been checked, order by decreaseing number of references to them

    active_tags = cursor.execute("SELECT * from Hashtag where checked == 0 AND ref >= ? ORDER BY ref DESC limit 1", (hashtag_ref_threshold,)) # todo: should use hashtag_ref_threshold
    active_tag_strings = [ str(tag[1]) for tag in active_tags]
    if(len(active_tag_strings) == 0):
        return False
    tweets = tag_query(active_tag_strings)
    tweets = filter_tweets(tweets, False)
    add_tweets_to_db(tweets, from_user_query=False)
    return True


def scrape_by_user():
    get_count_cursor = cursor.execute("SELECT count(*) from Username WHERE checked == 0 AND ref >= ? ORDER BY ref DESC limit 1", (user_ref_threshold,))
    for i in get_count_cursor:
        if i[0] == 0:
            return False

    active_users = cursor.execute("SELECT * from Username WHERE checked == 0 AND ref >= ? ORDER BY ref DESC limit 1", (user_ref_threshold,))
    tweets = user_query(active_users)
    tweets = filter_tweets(tweets, True)
    add_tweets_to_db(tweets, from_user_query=True)
    return True

def init():
    for data in cursor.execute("SELECT count(*) FROM Hashtag"):
        if data[0] == 0: # no initial hashtags
            print('REINITIALIZING DATABASE')
            time.sleep(5)
            for hashtag in ["trump", "donald","americanpolitics"]:
                query = "INSERT INTO Hashtag (hashtag,checked,ref) VALUES('{}',0,10000)".format(hashtag)
                cursor.execute(query)
                conn.commit()


    # for data in cursor.execute("SELECT count(*) FROM User"):
    #     if data[0] == 0: # no initial hashtags



def word_query(words):
    global keys

    for word in words:
        word_text = word[1]
        try:
            # get data from twitter using api
            tso = TwitterSearchOrder()
            tso.set_keywords([word_text]) # AND matching for keywords in list
            tso.set_language('en')
            tso.set_include_entities(False)
            ts = keys[0]
            tweets = ts.search_tweets_iterable(tso)
            # mark hashtag as checked
            mark_word_as_checked(word[0])
            return tweets
        except Exception as e:
            # if fail, move key[0] to end and sleep to allow key to reset
            print('switching keys')
            keys = keys[1:] + [keys[0]]
            time.sleep(10)
            tweets = []

    return []

def scrape_by_word():
    word_cursor = cursor.execute("SELECT * from SpecialWord WHERE checked == 0 AND ref >= ? ORDER BY ref DESC limit 1", (word_ref_threshold,))
    words = word_cursor.fetchall()

    tweets = word_query(words)
    tweets = filter_tweets(tweets, is_user=False)
    for tweet in tweets:
        branching_tags = create_branching_tags(str(tweet['retweeted_status']['text']))
        add_new_tags_to_db(branching_tags)


# MAIN
if __name__=="__main__":
    init()
    while True:

        if not scrape_by_tag() or not scrape_by_user():
        # if not scrape_by_user():

            print('scraping by wordish')
            scrape_by_word()
            time.sleep(5)
