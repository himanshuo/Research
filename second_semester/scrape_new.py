import sqlite3
import nltk
import os
import json
import time
import operator
import random
import math
import sys
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
    print('running tags from text: {}', txt)
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
    print('add new tags to db')
    for hashtag, ref in branching_tags.items():
        hashtag = hashtag.lower()
        num_seen = 0
        query_to_execute = "SELECT * FROM Hashtag WHERE hashtag = \"" + str(hashtag) + "\""
        #print "executing: " + query_to_execute
        for i in cursor.execute(query_to_execute):
            num_seen += i[3]


        if num_seen == 0:
            # query = "INSERT INTO Hashtag (hashtag,checked,ref) VALUES(?,0," + str(hashs[item]) + ")",(item,)
            query_to_execute = "INSERT INTO Hashtag (hashtag,checked,ref) VALUES(\"" + str(hashtag) + "\",0," + str(ref) + ")"
            #print "executing: " + query_to_execute
            cursor.execute(query_to_execute)

        else:
            # query = "UPDATE Hashtag SET ref = " + str(counter + hashs[item]) + " WHERE hashtag==\"" + item + "\""
            # query = "UPDATE Hashtag SET ref = {} WHERE hashtag=\""+hashtag+"\"".format(num_seen+ref)
            query_to_execute = "UPDATE Hashtag SET ref = " + str(num_seen + ref) + " WHERE hashtag=\"" + str(hashtag) + "\";"
            #print "executing: " + query_to_execute
            cursor.execute(query_to_execute)

        conn.commit()

def get_content_words(tokens):
    print("running method get_content_words")
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

def mark_tag_as_checked(hashtag):
    print("running method mark_tag_as_checked")
    # mark checked
    query_to_execute = "UPDATE Hashtag SET checked = 1 WHERE hashtag==\"" + str(hashtag)+ "\";"
    #print "executing: " + query_to_execute
    cursor.execute(query_to_execute)
    conn.commit()

def mark_user_as_checked(userid):
    print( "running method mark_user_as_checked: " + str(userid))
    # mark checked
    query_to_execute = "UPDATE Username SET checked = 1 WHERE userid==" + str(userid) + ";"
    #print "executing: " + query_to_execute
    cursor.execute(query_to_execute)
    conn.commit()

def mark_word_as_checked(word_id):
    print( "running method mark_word_as_checked")
    query_to_execute = "UPDATE SpecialWord SET checked = 1 WHERE id==" + str(word_id)+ ";"
    #print "executing: " + query_to_execute
    cursor.execute(query_to_execute)
    conn.commit()


def contains_key(mydict, mykey):
    #print "running method contains_key"
    try:
        mydict[mykey]
        return True
    except:
        return False

def is_new_tweet(tweet_text):
    tweet_text = tweet_text.replace("\"","'")
    """
        returns True if db does not contain this tweet already
    """
    print( "running method is_new_tweet")
    counting = 0
    # todo: turn this into a count query
    # todo: change counting to num_seen

    query_to_execute = "select * from Tweet where text == \"" + str(tweet_text)+ "\""
    #print "executing: " + query_to_execute
    for i in cursor.execute(query_to_execute):
        counting += 1
    return counting == 0




def meets_content_threshold(tweet_text_with_bad_chars):
    print( "running method meets_content_threshold")
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
        upsert_word(token)

def upsert_word(word):
    print( "upserting: " + word)
    # todo: there is probably a sqlite upsert function

    # num times user has been seen.
    count = 1
    query_to_execute = "SELECT * from SpecialWord WHERE word=\"" + str(word) + "\""
    #print "executing: " + query_to_execute
    for i in cursor.execute(query_to_execute):
        count += i[3]

    if count == 1:
        # add word if doesnt already exist
        query_to_execute = "INSERT INTO SpecialWord(word,checked,ref) Values(\"" + str(word) + "\",0,1);"
        #print "executing: " + query_to_execute
        cursor.execute(query_to_execute)
        conn.commit()
    else:
        # update that we saw this word once more
        # cursor.execute("UPDATE SpecialWord SET ref = " + str(count) + " WHERE word==\"" + str(word) + "\";")
        query_to_execute = "UPDATE SpecialWord SET ref = " + str(count) + " where word==\"" + str(word) + "\""
        #print "executing: " + query_to_execute
        cursor.execute(query_to_execute)
        conn.commit()


def filter_tweets(tweets, is_user):
    out = []
    if is_user:
        for tweet in tweets:
            try:
                a = str(tweet['text'])
            except:
                continue
            if tweet['retweet_count'] > retweet_count_threshold and \
                not contains_key(tweet, 'retweeted_status') and \
                is_new_tweet(tweet['text']) and \
                tweet['user']['followers_count'] > follower_count_threshold and \
                meets_content_threshold(tweet['text']):
                    out.append(tweet)
    else:
        for tweet in tweets:
            try:
                a = str(tweet['retweeted_status']['text'])
            except:
                continue
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
    query_to_execute ="SELECT * from Username WHERE userid==" + str(username_id) + ";"
    #print "executing: " + query_to_execute
    for i in cursor.execute(query_to_execute):
        count += i[4]

    if count == 1:
        # add user if doesnt already exist
        print( "user does not already exist")
        query_to_execute = "INSERT INTO Username(userid, follower_count, username, checked, ref) Values(" + str(username_id) + "," + str(username_followers) + ",\"" + str(username_name) + "\",0,1);"
        #print "executing: " + query_to_execute
        cursor.execute(query_to_execute)
        conn.commit()
    else:
        # update that we saw this user once more
        query_to_execute = "UPDATE Username SET ref = " + str(count) + " WHERE userid==" + str(username_id) + ";"
        #print "executing: " + query_to_execute
        cursor.execute(query_to_execute)
        conn.commit()


def add_tweets_to_db(tweets, from_user_query):
    print( "called method add_tweets_to_db")
    for tweet in tweets:
        # add each tweet to db.
        # this will likely break for whatever reasons.
        # ignore tweets that break
        try:

            add_tweet_to_db(tweet, from_user_query)
        except:
            print("failed to add: {}".format(str(tweet)))

def create_branching_tags(tweet_text):
    print( "called method branching tags")
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
    print('adding tweet to db')
    # get database stuff
    if not from_user_query:
        username_name = str(tweet['retweeted_status']['user']['screen_name'])
        username_id = int(tweet['retweeted_status']['user']['id'])
        username_followers = int(tweet['retweeted_status']['user']['followers_count'])
        tweet_text = str(tweet['retweeted_status']['text'])
        print( tweet_text)
        tweet_text = tweet_text.replace("\"","'")
        print( tweet_text)
        tweet_retweets = int(tweet['retweeted_status']['retweet_count'])
        tweet_favorites = int(tweet['retweeted_status']['favorite_count'])
        tweet_twitterid = int(tweet['retweeted_status']['id'])
        # tweet_created_at = str(tweet['retweeted_status']['created_at'])
        created_at_datetime = datetime.datetime.strptime(tweet['retweeted_status']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        tweet_created_at = (created_at_datetime-datetime.datetime(1970,1,1)).total_seconds()
    else:
        username_name = str(tweet['user']['screen_name'])
        username_id = int(tweet['user']['id'])
        username_followers = int(tweet['user']['followers_count'])
        tweet_text = str(tweet['text'])
        print( tweet_text)
        tweet_text = tweet_text.replace("\"","'")
        print( tweet_text)
        tweet_retweets = int(tweet['retweet_count'])
        tweet_favorites = int(tweet['favorite_count'])
        tweet_twitterid = int(tweet['id'])
        # tweet_created_at = str(tweet['retweeted_status']['created_at'])
        created_at_datetime = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        tweet_created_at = (created_at_datetime-datetime.datetime(1970,1,1)).total_seconds()

    #add associate user
    upsert_user(username_id, username_name, username_followers)
    # add tweet into db
    query_to_execute = "INSERT INTO Tweet (username,text,retweet_count,favorite_count,twitterID,created_at) Values" \
        "(\"" + str(username_name) + "\",\"" + str(tweet_text) + "\"," + str(tweet_retweets) + "," + str(tweet_favorites) + "," + str(tweet_twitterid) + ",\"" + str(tweet_created_at) + "\");"
    #print "executing: " + query_to_execute
    cursor.execute(query_to_execute)
    conn.commit()

    # add hashtags to db
    branching_tags = create_branching_tags(tweet_text)
    add_new_tags_to_db(branching_tags)

    # add special words to db
    add_special_words(tweet_text)
    print( "done adding from ")
    print(tweet_text)




def tag_query(active_tags):
    print('tag query')
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
    #print "doing method: get_two_week_old_tweet_id()"
    two_weeks_ago = (datetime.datetime.now() - datetime.timedelta(days=20))
    epoch = datetime.datetime.utcfromtimestamp(0)
    two_weeks_ago_seconds_since_epoch = (two_weeks_ago - epoch).total_seconds() * 1000.0

    try:
        query_to_execute = "SELECT twitterID,created_at from tweet WHERE created_at >= " + str(two_weeks_ago_seconds_since_epoch) + " order by created_at limit 1;"
        #print "executing: " + query_to_execute
        for i in cursor.execute(query_to_execute):
            return i[0]
    except:
        return 0

def user_query(active_users):
    global keys
    #print "doing method user_query"
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
    #print "returned from user_query"
    return tweets

def scrape_by_tag():
    # determine which tags to look for. tags that havent already been checked, order by decreaseing number of references to them
    print('scraping by tag')
    query_to_execute = "SELECT * from Hashtag where checked == 0 AND ref >= " + str(hashtag_ref_threshold) + " ORDER BY ref DESC limit 1;"
    #print "executing: " + query_to_execute
    active_tags = cursor.execute(query_to_execute)
    active_tag_strings = [ str(tag[1]) for tag in active_tags]
    if(len(active_tag_strings) == 0):
        return False
    #print('found {} tags to query for', len(active_tag_strings))
    tweets = tag_query(active_tag_strings)
    tweets = filter_tweets(tweets, False)
    add_tweets_to_db(tweets, from_user_query=False)
    return True


def scrape_by_user():
    print('scraping by user')
    query_to_execute = "SELECT count(*) from Username WHERE checked == 0 AND ref >= " + str(user_ref_threshold) + " ORDER BY ref DESC limit 1;"
    #print "executing: " + query_to_execute
    get_count_cursor = cursor.execute(query_to_execute)
    for i in get_count_cursor:
        if i[0] == 0:
            return False
    query_to_execute = "SELECT * from Username WHERE checked == 0 AND ref >= " + str(user_ref_threshold) + " ORDER BY ref DESC limit 1;"
    #print "executing: " + query_to_execute
    active_users = cursor.execute(query_to_execute)
    tweets = user_query(active_users)
    tweets = filter_tweets(tweets, True)
    add_tweets_to_db(tweets, from_user_query=True)
    return True

def init():
    print( "running init()")
    for data in cursor.execute("SELECT count(*) FROM Hashtag"):
        if data[0] == 0: # no initial hashtags
            print('REINITIALIZING DATABASE')
            time.sleep(5)
            for hashtag in seed_hashtags:
                print( "adding: #" + str(hashtag) + " into db")
                query_to_execute = "INSERT INTO Hashtag (hashtag,checked,ref) VALUES(\"" + str(hashtag) + "\",0,10000);"
                print( "executing: " + query_to_execute)
                cursor.execute(query_to_execute)
                conn.commit()
    print( "exited from init()")


def word_query(words):
    global keys
    #print "starting word queries"
    for word in words:
        word_text = word[1]
        #print('querying for word {}', format(word_text))
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
            #print "sucessefully returned from word_query"
            return tweets
        except Exception as e:
            # if fail, move key[0] to end and sleep to allow key to reset
            print('switching keys')
            keys = keys[1:] + [keys[0]]
            time.sleep(10)
    return []

def scrape_by_word():
    print('scraping by word')
    query_to_execute = "SELECT * from SpecialWord WHERE checked == 0 AND ref >= " + str(word_ref_threshold) + " ORDER BY ref DESC limit 1;"
    #print "executing: " + query_to_execute
    word_cursor = cursor.execute(query_to_execute)
    words = word_cursor.fetchall()
    #print('found {} words to scrape'.format(len(words)))
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
            scrape_by_word()
            time.sleep(5)
