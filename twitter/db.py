#!/usr/bin/python

from models import engine, User, Tweet, Hashtag
import pprint
import sys
import string
import datetime
import pytz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlite3
from constants import DB_USER, DB_PASSWD, DB_HOST, DB_NAME
import mysql.connector

# create a configured "Session" class
Session = scoped_session(sessionmaker(bind=engine))

class DB:
    def __init__(self):
        try:
            # create a Session
            self.session = Session()
        except:
            print('could not connect to sqlite db')


        config = {
                      'user': DB_USER,
                      'password': DB_PASSWD,
                      'host': DB_HOST,
                      'database': DB_NAME,
                    }

        db = mysql.connector.connect(**config)
        self.mysql_cur = db.cursor()




    def twitter_to_mysql_timestamp(self,twitter_time):
        if (not (twitter_time is None)) and (not (twitter_time == "")):
            tweet_date = datetime.datetime.strptime(twitter_time,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
        else:
            tweet_date = None
        return tweet_date


    def ascii_string(self, s):
        return ''.join(filter(lambda x: x in string.printable, s))


    def add_twitter_data(self, twitter_data):


        remote_user = twitter_data.get('user')
        try:
            user = self.session.query(User).filter(User.id == remote_user.get('id_str')).one()
        except:

            user = User(
                id = remote_user.get('id_str'),
                name=self.ascii_string( remote_user.get('name', None)),
                screen_name=remote_user.get('screen_name', None),
                followers=remote_user.get('followers_count', None),
                friends=remote_user.get('friends_count', None),
                favorites=remote_user.get('favourites_count',None),
                statuses=remote_user.get('statuses_count',None),
                created_at = self.twitter_to_mysql_timestamp(remote_user.get('created_at',None)),
            )


        try:
            self.session.query(Tweet).filter(Tweet.id == twitter_data.get('id',None)).one()
            #if we are able to query than tweet already exists. ignore this tweet.
            return
        except:
            #else continue normally.
            pass

        tweet = Tweet(
            id = self.ascii_string(twitter_data.get('id_str',None)),
            created_at = self.twitter_to_mysql_timestamp(twitter_data.get('created_at',None)),
            text = self.ascii_string( twitter_data.get('text') ),


            geo = self.ascii_string(str(twitter_data.get('geo', None))),
            coordinates = self.ascii_string(str(twitter_data.get('coordinates', None))),
            place =  self.ascii_string(str(twitter_data.get('place', None))),

            retweet_count = twitter_data.get('retweet_count', None),
            favorite_count = twitter_data.get('favorite_count', None),
        )
        user.tweets.append(tweet)




        remote_tags = twitter_data.get('entities').get('hashtags')

        for t in remote_tags:
            try:

                tag_text = self.ascii_string(t.get('text',''))
                try:
                    db_tag = self.session.query(Hashtag).fileter(Hashtag.text == tag_text).one()
                except:
                    db_tag = Hashtag(
                        text=tag_text
                    )

                tweet.hashtags.append(db_tag)

            except:
                print("Unexpected error:", sys.exc_info()[0])
                print(twitter_data)


        self.session.add(user)
        self.session.commit()

    def get_tweet(self, text, user_id):
        #todo: this method should allow you to put in a bunch of
        #todo: random params and get the appropriately matching tweets.
        # self.cur.execute("SELECT * FROM Tweet where text=%s", [text])
        pass

    def get_tweets(self, num=None):
        # #todo: make smarter. allow for getting user, and hashtags.
        # query = "SELECT * FROM Tweet"
        # if num:
        #     query + " LIMIT " + str(num)
        # self.cur.execute(query)
        # return self.cur.fetchall()
        pass

    def print_tweets(self, num=None):
        # tweets = self.get_tweets(num)
        # pprint.pprint(tweets)
        pass

    def print_schema(self):
        # print("-----------------Tweet-----------------")
        # self.cur.execute("DESCRIBE Tweet")
        # pprint.pprint(self.cur.fetchall())
        #
        # print("-----------------User-----------------")
        # self.cur.execute("DESCRIBE User")
        # pprint.pprint(self.cur.fetchall())
        #
        # print("-----------------HashTag-----------------")
        # self.cur.execute("DESCRIBE HashTag")
        # pprint.pprint(self.cur.fetchall())
        #
        # print("-----------------HashTagTweet-----------------")
        # self.cur.execute("DESCRIBE HashTagTweet")
        # pprint.pprint(self.cur.fetchall())
        pass


    # todo: currently, this only works for a single ho2es sqlite db.
    # todo: I need it to get data from hcdm mysql and hcdm sqlite
    """
    Things to Consider:
    1) which database to get data from
    2) num tweets to get
    3) filter tweets by:
            1) user
                1)user name
                2)user location
                3)user num followers
                4)user num friends
                5)user num favorites
                6)user num statuses
                7)user create at
            2) hashtag
                1)text
            3) tweet
                1)created at
                2)text
                3)some phrase inside text
                4)geo
                5)coordinates
                6)place
                7)retweet count
                8)favorite count
    """

    def get_mysql_data(self, query):
        self.mysql_cur.execute(query)
        return self.mysql_cur.fetchall()




    def tweets(self, detail=False):
        """
        generator that returns tweets one by one
        :return:
        """


        #ho2es sqlite
        to_get = Tweet if detail else Tweet.text
        for tweet in self.session.query(to_get):
            yield tweet[0]

        #hcdm sqlite
        path_to_hcdm_sqlite = './data/hcdm_sqlite'
        conn = sqlite3.connect(path_to_hcdm_sqlite)
        c = conn.cursor()
        query = 'SELECT {} FROM tweet'.format('*' if detail else 'text')
        for row in c.execute(query):
            yield row
        conn.close()


        #hcdm mysql (converted to sqlite)
        # path_to_hcdm_mysql = './data/hcdm_mysql'
        # conn = sqlite3.connect(path_to_hcdm_mysql)
        # c = conn.cursor()
        # query = 'SELECT {} FROM tweet'.format('*' if detail else 'text')
        # for row in c.execute(query):
        #     yield row
        # conn.close()



        # sample data
        # for tweet in ["hi my name-is himanshu"]:
        #     yield tweet


if __name__=="__main__":
    pass
    # db = DB()
    # tweet = {
    #     "created_at": "Thu Apr 02 22:16:15 +0000 2015",
    #     "id": 583754843887571000,
    #     "id_str": "583754843887570945",
    #     "text": "Wake up eat watermelon then go to basketball practice",
    #     "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
    #     "truncated": False,
    #     "in_reply_to_status_id": None,
    #     "in_reply_to_status_id_str": None,
    #     "in_reply_to_user_id": None,
    #     "in_reply_to_user_id_str": None,
    #     "in_reply_to_screen_name": None,
    #     "user": {
    #         "id": 2950893090,
    #         "id_str": "2950893090",
    #         "name": "Diego Coronado",
    #         "screen_name": "D_Coronado5",
    #         "location": "",
    #         "url": None,
    #         "description": "gabriela❤️ \njust trying to make it",
    #         "protected": False,
    #         "verified": False,
    #         "followers_count": 99,
    #         "friends_count": 89,
    #         "listed_count": 0,
    #         "favourites_count": 265,
    #         "statuses_count": 235,
    #         "created_at": "Mon Dec 29 21:10:03 +0000 2014",
    #         "utc_offset": None,
    #         "time_zone": None,
    #         "geo_enabled": True,
    #         "lang": "en",
    #         "contributors_enabled": False,
    #         "is_translator": False,
    #         "profile_background_color": "C0DEED",
    #         "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
    #         "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
    #         "profile_background_tile": False,
    #         "profile_link_color": "0084B4",
    #         "profile_sidebar_border_color": "C0DEED",
    #         "profile_sidebar_fill_color": "DDEEF6",
    #         "profile_text_color": "333333",
    #         "profile_use_background_image": True,
    #         "profile_image_url": "http://pbs.twimg.com/profile_images/567430130197229568/p_T9pyJF_normal.jpeg",
    #         "profile_image_url_https": "https://pbs.twimg.com/profile_images/567430130197229568/p_T9pyJF_normal.jpeg",
    #         "profile_banner_url": "https://pbs.twimg.com/profile_banners/2950893090/1419888436",
    #         "default_profile": True,
    #         "default_profile_image": False,
    #         "following": None,
    #         "follow_request_sent": None,
    #         "notifications": None
    #     },
    #     "geo": None,
    #     "coordinates": None,
    #     "place": None,
    #     "contributors": None,
    #     "retweet_count": 0,
    #     "favorite_count": 0,
    #     "entities": {
    #         "hashtags": [],
    #         "trends": [],
    #         "urls": [],
    #         "user_mentions": [],
    #         "symbols": []
    #     },
    #     "favorited": False,
    #     "retweeted": False,
    #     "possibly_sensitive": False,
    #     "filter_level": "low",
    #     "lang": "en",
    #     "timestamp_ms": "1428012975080"
    # }
    # db.add_twitter_data(tweet)
    # db.print_tweets()
    
    


