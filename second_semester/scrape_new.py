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
import unigrammodel
from TwitterSearch import *

tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()


# filtered out
stopwords = ['i','to','the','a','and','in','you','my','of','it','for','is','on','that','this','me']
punctuations = ['``',':','!','.',',','&','(',')','*','^','%','$','#','@','~','""',';','<','>','/','?','...','-']

retweet_count_threshold = 10 # atleast 10 retweets
follower_count_threshold = 100 # atleast 100 followers
content_threshold = 10  # atleast 10 remaining content words (after filtering)


# keys

ts1 = TwitterSearch(
    consumer_key = 'nr2GFw3XVpNOSD9ZOlddfhGxq',
    consumer_secret = 'UCv6lKJXjRJyIvtOYdSoIBWzusfp4Iy6zAE5UGAM8dhEk8Svp8',
    access_token = '4549049355-hpKIheHy9JGVRrDnsCv6iF7Sf2EoHglbnJTl9Y3',
    access_token_secret = 'oWMgAgzW0RMyx94jSrMoJxDrSOZPvUHykvs8M2dDHWjMw'
)

ts2 = TwitterSearch(
    consumer_key = 'bIblpmxgiTBOgmsDtSyEkj79f',
    consumer_secret = 'XWQs98ZIBBuD1hJ0wuHRNfWw9f5SjDplyYdljQqZ57onXkNQqK',
    access_token = '4549049355-NRCTfBlktXDb9H0ENsOZVj3YZrBWVbVvIRRv6yr',
    access_token_secret = 'RRH8ksVn6McAXoChh6Z6PYgyS2mHA7tcCxX1JPV7t77Dc'
)

ts3 = TwitterSearch(
    consumer_key = 'LmKNKUYpwgmdKzu2KsBhHk5zn',
    consumer_secret = '3wcePG0IDwtfNMXt1mbs4DZK3xfv28DVxarmsK8mzlC7HBbN3B',
    access_token = '4549049355-TF4DjiXRjl6buXcQWREpYMuGGNe6ceY3up1aREo',
    access_token_secret = 'F7hHW7Q0uMPMMloaP4l4J3vAjDyNnvtiFsNCJ86Z2dYm9'
)

ts4 = TwitterSearch(
    consumer_key = 'vUPxVFAtrLtKicCTLdKebmtMz',
    consumer_secret = 'jNztwiJJsXMpK1n7zIpajTZVp4q2pvdLuCJZ0PUVXpmvubv1Qr',
    access_token = '4549049355-xEg0t50dljrofN9jGOaJZITKsqqO9dTMVhafAfZ',
    access_token_secret = 'wnH6gjWxMcso9y3H7kJoGIOPHA1LlKuQfl3TSa1sGonJB'
)

ts5 = TwitterSearch(
    consumer_key = 'Uyh9UjqNLI85SPcFWj83yYgCk',
    consumer_secret = 'snvA1xYmpayuXcDwavEAjnnockIyRBo7cMSdO8EbvRwmBQCKDg',
    access_token = '4569957028-E9qX8y96tKFS9ylK58E1raUU5j5Z6aP5rcoouGH',
    access_token_secret = 'sCr2f3YaZfZF42nIfnVLSEPV0Tkbru3fiNAWdDHyQzURQ'
)

ts6 = TwitterSearch(
    consumer_key = 'tpqNFMMlg2MuHW70EJBC1bJ9A',
    consumer_secret = 'LBPhWbGolH4ohQfyCcAnPLSBx4fklksyerhUGSqiHOeEdU8jFO',
    access_token = '4569957028-5Fy3y1pdT2OBHYriYK1W1w3UPlqou1e7TPqqpGG',
    access_token_secret = 'eUQQGaeXjoO2hlp1XGXGDRB8yBKBsszfUusJbFFrRLbUk'
)

ts7 = TwitterSearch(
    consumer_key = 'W85OOlizRjcIaFwLG6XpC9u2v',
    consumer_secret = '9AJKgaqNXK8tHhPEEHOe8BFk82B2JhVtOCXlrFDf8b5mDIfpwV',
    access_token = '4569957028-YE6dRXp4KcVvy2rskN8WtL3ojVqhyHVJwhHZgLu',
    access_token_secret = '5DoMvgRo21LHm4HRtJqMQ8evs756umfcdKzRQJThr8FWO'
)

ts8 = TwitterSearch(
    consumer_key = '2I6HK4aRWuYhSNENiH487VRhk',
    consumer_secret = 'sW3zBQLSHcuc32AcWQUdFpwRWFel7X2siR55v3FE62hz5hNNsm',
    access_token = '4569931877-OLHVuav8XmHsHdRh3RUGI5zdrjlLFVwrliIxkJk',
    access_token_secret = '8qspicVCzhdFeA9Plq6lGjubBEnINM0AqPS3i2jDwe93h'
)

ts9 = TwitterSearch(
    consumer_key = 'Oa89wcEJzsqVJ7CGLINzYJY6o',
    consumer_secret = 'QtkHjT4g7WwSHlhbqyBmDuSbpxR46TCVLSfgXSICpB74mCu9ek',
    access_token = '4569931877-tmLgt1pAXAMx4IWkSXOYMORElxN72qar4p2j22B',
    access_token_secret = 'XeP9knsl4iuwvTWg4OuhTISXSaqpbN5s8UKwYrA0TQj7B'
)

ts10 = TwitterSearch(
    consumer_key = 'Yf6df4Awqpt44UL7mxxK0avLP',
    consumer_secret = 'EUHH9qXDLi3PGaBEHSXDqWxlHmFJ3K8733skzNFCjtqaC0q2Q6',
    access_token = '4569931877-s6D15iiRI1OaQYoRI8HCh2KUpE0Q1eqC8NZF3sf',
    access_token_secret = 'qtBIKYd7bnQcsMslEaqpXXEkSUvAJg3TlBgPbEvVA1Czf'
)

keys = [ts1,ts2,ts3,ts4,ts5,ts6,ts7,ts8,ts9,ts10]


conn2 = sqlite3.connect('new_tweets.db')
c2 = conn2.cursor()

def scrape_tags(tweet):
    """
    tweet text -> [hashtags in tweet]
    """
    try:
        tweet = str(tweet)
        hashs = []
        hashtag = False
        for token in tokenizer.tokenize(tweet):
            if token == "#":
                hashtag = True
            if token != "#" and hashtag:
                hashs.append(token)
                hashtag = False
        return hashs
    except:
        return []

def add_new_tags_to_db(hashs,conn,c):
    """
        hashs: dict of hashtags
        c, conn: both connection variables
        if new tag, then add to db
        else modify db to reflect that this dict of hashtags has been seen more times
    """
    print hashs
    for item in hashs:
        item = item.lower()
        counter = 0
        for i in c.execute("SELECT * FROM Hashtag WHERE hashtag == ?",(item,)):
            counter += i[3]
        if counter == 0:
            c.execute("INSERT INTO Hashtag (hashtag,checked,ref) VALUES(?,0," + str(hashs[item]) + ")",(item,))
            conn.commit()
        else:
            c2.execute("UPDATE Hashtag SET ref = " + str(counter + hashs[item]) + " WHERE hashtag==\"" + item + "\"")
            conn2.commit()

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


# MAIN

while True:
    # determine which tags to look for. tags that havent already been checked, order by decreaseing number of references to them
    active_tags = c2.execute("SELECT * from Hashtag where checked == 0 ORDER BY ref DESC limit 1")

    for tag in [x for x in active_tags if x]:
        # scrape every 5 seconds
        time.sleep(5)


        # get new hashtag to scrape

        # build hashtag in proper format
        hashtag = "#" + str(tag[1])
        # mark checked
        c2.execute("UPDATE Hashtag SET checked = 1 WHERE hashtag==\"" + tag[1] +"\"")
        conn2.commit()


        #  scrape data
        tweets = []
        try:
            tso = TwitterSearchOrder()
            tso.set_keywords([hashtag]) # AND matching for keywords in list
            tso.set_language('en')
            tso.set_include_entities(False)
            branching_tags = {}
            ts = keys[0]
            tweets = ts.search_tweets_iterable(tso)
        except Exception as e:
            # print(e)
            # print "ooops out of requests, pausing for 1 minute"
            # print "switching keys"
            # move key[0] to end
            keys = keys[1:] + [keys[0]]
            # if fail, then say that we havent checked
            c2.execute("UPDATE Hashtag SET checked = 0 WHERE hashtag==\"" + tag[1] +"\"")
            conn2.commit()
            time.sleep(10)


        # process scrape data
        for tweet in tweets:
            if tweet['retweet_count'] > retweet_count_threshold:

                # contains retweeted_status
                retweeted_status = False
                try:
                    c = tweet['retweeted_status']
                    retweeted_status = True
                except:
                    retweeted_status = False

                if retweeted_status:
                    # if already exists in database with exact same text, then dont use it
                    counting = 0
                    for i in c2.execute("select * from Tweet where text == ?",(tweet['retweeted_status']['text'],)):
                        counting += 1
                    if counting == 0 and tweet['retweeted_status']['user']['followers_count'] > follower_count_threshold:

                        #
                        try:
                            # throws out bad characters. if conversion fails, we ignore entire tweet
                            text = str(tweet['retweeted_status']['text'])

                            # get content of tweet
                            tokens = tokenizer.tokenize(text)
                            new_tokens = get_content_words(tokens)
                            # more filtering to tweet based on contents of tweet
                            if len(new_tokens) > content_threshold:

                                # IF YOU ARE THIS FAR, tweet is good.

                                # get database stuff
                                username_name = str(tweet['retweeted_status']['user']['screen_name'])
                                username_id = str(tweet['retweeted_status']['user']['id'])
                                username_followers = str(tweet['retweeted_status']['user']['followers_count'])
                                tweet_text = str(tweet['retweeted_status']['text'])
                                tweet_retweets = str(tweet['retweeted_status']['retweet_count'])
                                tweet_favorites = str(tweet['retweeted_status']['favorite_count'])
                                tweet_twitterid = str(tweet['retweeted_status']['id'])

                                # num times user has been seen.
                                count = 1
                                for i in c2.execute("SELECT * from Username WHERE userid==" + str(username_id) + ";"):
                                    count += i[4]

                                if count == 1:
                                    # add user if doesnt already exist
                                    c2.execute("INSERT INTO Username Values(" + username_id + "," + username_followers + ",\"" + username_name + "\",0,1);")
                                    conn2.commit()
                                else:
                                    # update that we saw this user once more
                                    c2.execute("UPDATE Username SET ref = " + str(count) + " WHERE userid==" + str(username_id) + ";")
                                    conn2.commit()

                                # add tweet into db
                                c2.execute("INSERT INTO Tweet (username,text,retweet_count,favorite_count,twitterID) Values(" + username_id + ",?," + tweet_retweets + "," + tweet_favorites + "," + tweet_twitterid + ")",(tweet_text,))
                                conn2.commit()

                                # list of hashtags in tweet
                                # branching_tags: {hashtags: ref}
                                # if exists in branching tags, then increment counter, else add to branching tags with ref=1
                                scraped = scrape_tags(tweet['retweeted_status']['text'])
                                for item in scraped:
                                    try:
                                        branching_tags[item.lower()] += 1
                                    except:
                                        branching_tags[item.lower()] = 1
                        except:
                            print ""

        add_new_tags_to_db(branching_tags,conn2,c2)

    # SAME PROCESS but with username and users history
    # todo: cut off user history by some feature (1 month, num tweets)
    active_users = c2.execute("SELECT * from Username WHERE checked == 0 limit 1")
    for user in active_users:
        user = str(user[2])
        c2.execute("UPDATE Username SET checked = 1 WHERE username==\"" + user + "\"")
        conn2.commit()
        tweets = []
        try:
            tuo = TwitterUserOrder(user)
            # todo: search_tweets_iterable gets all historical tweets of user in chunks. Perhaps stop getting more chunks if x condition
            tweets = ts.search_tweets_iterable(tuo)
        except Exception as e:
            print(e)
            print "ooops out of requests, pausing for 1 minute"
            print "switching keys"
            keys = keys[1:] + [keys[0]]
            c2.execute("UPDATE Username SET checked = 0 WHERE username==\"" + user +"\"")
            conn2.commit()
            time.sleep(10)
        branching_tags = {}
        for tweet in tweets:
            if tweet['retweet_count'] > retweet_count_threshold:
                retweeted_status = False
                try:
                    c = tweet['retweeted_status']
                    retweeted_status = True
                except:
                    retweeted_status = False
                if retweeted_status:
                    counting = 0
                    for i in c2.execute("select * from Tweet where text == ?",(tweet['retweeted_status']['text'],)):
                        counting += 1
                    if tweet['retweeted_status']['user']['followers_count'] > follower_count_threshold and counting == 0:
                        try:
                            text = str(tweet['retweeted_status']['text'])
                            tokens = tokenizer.tokenize(text)
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
                                        new_tokens.append(token.lower())
                            if len(new_tokens) > content_threshold:
                                username_name = str(tweet['retweeted_status']['user']['screen_name'])
                                username_id = str(tweet['retweeted_status']['user']['id'])
                                username_followers = str(tweet['retweeted_status']['user']['followers_count'])
                                tweet_text = str(tweet['retweeted_status']['text'])
                                tweet_retweets = str(tweet['retweeted_status']['retweet_count'])
                                tweet_favorites = str(tweet['retweeted_status']['favorite_count'])
                                tweet_twitterid = str(tweet['retweeted_status']['id'])
                                count = 0
                                for i in c2.execute("SELECT * from Username WHERE userid==" + str(username_id) + ";"):
                                    count += 1
                                if count == 0:
                                    c2.execute("INSERT INTO Username Values(" + username_id + "," + username_followers + ",\"" + username_name + "\",0);")
                                    conn2.commit()
                                c2.execute("INSERT INTO Tweet (username,text,retweet_count,favorite_count,twitterID) Values(" + username_id + ",?," + tweet_retweets + "," + tweet_favorites + "," + tweet_twitterid + ")",(tweet_text,))
                                conn2.commit()
                                scraped = scrape_tags(tweet['retweeted_status']['text'])
                                for item in scraped:
                                    try:
                                        branching_tags[item.lower()] += 1
                                    except:
                                        branching_tags[item.lower()] = 1
                        except:
                            print ""
        add_new_tags_to_db(branching_tags,conn2,c2)
    conn2.commit()
