#!/usr/bin/python
import MySQLdb
from constants import DB_NAME, DB_HOST, DB_USER, DB_PASSWD
import pprint
import sys
import string
class DB:
    def __init__(self):
        try:
            self.db = MySQLdb.connect(host=DB_HOST,
                         user=DB_USER,
                          passwd=DB_PASSWD,
                          db=DB_NAME)
            self.cur = self.db.cursor(MySQLdb.cursors.DictCursor)
            # TABLES:   Tweet, HashTag, HashTagTweet, User
        except:
            print('could not connect to db')

    def ascii_string(self, s):
        return ''.join(filter(lambda x: x in string.printable, s))


    def add_twitter_data(self, twitter_data):

        user = twitter_data.get('user')
        user_insert_query = """
                             INSERT INTO User (
                             name,
                             followers_count,
                             friends_count,
                             listed_count,
                             favorites_count,
                             statuses_count,
                             created_at
                             ) VALUES (%s, %s, %s, %s, %s, %s, %s )
                             """
        try:
            self.cur.execute(user_insert_query,
                             (
                                self.ascii_string( user.get('name', None) ),
                                user.get('followers_count',None),
                                user.get('friends_count',None),
                                user.get('listed_count',None),
                                user.get('favourites_count',None),
                                user.get('statuses_count',None),
                                user.get('created_at',None),

                            )
            )
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(twitter_data)



        user_id = self.cur.lastrowid
        tweet_insert_query = """
                            INSERT INTO Tweet (
                             text,
                             source,
                             user_id,
                             geo,
                             coordinates,
                             place,
                             retweet_count,
                             favorite_count,
                             timestamp
                             ) VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s)
                            """

        try:
            self.cur.execute(tweet_insert_query,
                             ( self.ascii_string( twitter_data.get('text') ),
                              self.ascii_string( twitter_data.get('source',None) ),
                              twitter_data.get(user_id),
                              self.ascii_string(str(twitter_data.get('geo', None))),
                              self.ascii_string(str(twitter_data.get('coordinates', None))),
                              self.ascii_string(str(twitter_data.get('place', None))),
                              twitter_data.get('retweet_count', None),
                              twitter_data.get('favorite_count', None),
                              twitter_data.get('created_at', None),
                             )
            )
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(twitter_data)



        tweet_id = self.cur.lastrowid
            
        tags = twitter_data.get('entities').get('hashtags')

        for t in tags:
            try:
                #todo: handle duplicates
                self.cur.execute("INSERT INTO HashTag (tag) VALUES(%s)" , [ self.ascii_string( t.get('text','')) ])
            except:
                print("Unexpected error:", sys.exc_info()[0])
                print(twitter_data)



            hashtag_id = self.cur.lastrowid
            try:
                self.cur.execute("INSERT INTO HashTagTweet (hashtag_id, tweet_id) VALUES (%s, %s)",
                                 (hashtag_id, tweet_id)
                )
            except:
                print("Unexpected error:", sys.exc_info()[0])
                print(twitter_data)


        self.db.commit()

    def get_tweet(self, text, user_id):
        #todo: this method should allow you to put in a bunch of
        #todo: random params and get the appropriately matching tweets.
        self.cur.execute("SELECT * FROM Tweet where text=%s", [text])

    def get_tweets(self, num=None):
        #todo: make smarter. allow for getting user, and hashtags.
        query = "SELECT * FROM Tweet"
        if num:
            query + " LIMIT " + str(num)
        self.cur.execute(query)
        return self.cur.fetchall()

    def print_tweets(self, num=None):
        tweets = self.get_tweets(num)
        pprint.pprint(tweets)

    def print_schema(self):
        print("-----------------Tweet-----------------")
        self.cur.execute("DESCRIBE Tweet")
        pprint.pprint(self.cur.fetchall())

        print("-----------------User-----------------")
        self.cur.execute("DESCRIBE User")
        pprint.pprint(self.cur.fetchall())

        print("-----------------HashTag-----------------")
        self.cur.execute("DESCRIBE HashTag")
        pprint.pprint(self.cur.fetchall())

        print("-----------------HashTagTweet-----------------")
        self.cur.execute("DESCRIBE HashTagTweet")
        pprint.pprint(self.cur.fetchall())




if __name__=="__main__":
    db = DB()
    tweet = {
        "created_at": "Thu Apr 02 22:16:15 +0000 2015",
        "id": 583754843887571000,
        "id_str": "583754843887570945",
        "text": "Wake up eat watermelon then go to basketball practice",
        "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
        "truncated": False,
        "in_reply_to_status_id": None,
        "in_reply_to_status_id_str": None,
        "in_reply_to_user_id": None,
        "in_reply_to_user_id_str": None,
        "in_reply_to_screen_name": None,
        "user": {
            "id": 2950893090,
            "id_str": "2950893090",
            "name": "Diego Coronado",
            "screen_name": "D_Coronado5",
            "location": "",
            "url": None,
            "description": "gabriela❤️ \njust trying to make it",
            "protected": False,
            "verified": False,
            "followers_count": 99,
            "friends_count": 89,
            "listed_count": 0,
            "favourites_count": 265,
            "statuses_count": 235,
            "created_at": "Mon Dec 29 21:10:03 +0000 2014",
            "utc_offset": None,
            "time_zone": None,
            "geo_enabled": True,
            "lang": "en",
            "contributors_enabled": False,
            "is_translator": False,
            "profile_background_color": "C0DEED",
            "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
            "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
            "profile_background_tile": False,
            "profile_link_color": "0084B4",
            "profile_sidebar_border_color": "C0DEED",
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_text_color": "333333",
            "profile_use_background_image": True,
            "profile_image_url": "http://pbs.twimg.com/profile_images/567430130197229568/p_T9pyJF_normal.jpeg",
            "profile_image_url_https": "https://pbs.twimg.com/profile_images/567430130197229568/p_T9pyJF_normal.jpeg",
            "profile_banner_url": "https://pbs.twimg.com/profile_banners/2950893090/1419888436",
            "default_profile": True,
            "default_profile_image": False,
            "following": None,
            "follow_request_sent": None,
            "notifications": None
        },
        "geo": None,
        "coordinates": None,
        "place": None,
        "contributors": None,
        "retweet_count": 0,
        "favorite_count": 0,
        "entities": {
            "hashtags": [],
            "trends": [],
            "urls": [],
            "user_mentions": [],
            "symbols": []
        },
        "favorited": False,
        "retweeted": False,
        "possibly_sensitive": False,
        "filter_level": "low",
        "lang": "en",
        "timestamp_ms": "1428012975080"
    }
    db.add_twitter_data(tweet)
    db.print_tweets()
    
    


