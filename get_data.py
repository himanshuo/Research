from __future__ import absolute_import, print_function
from constants import *

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


import json
import pprint


# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=CONSUMER_KEY
consumer_secret=CONSUMER_SECRET

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=OAUTH_TOKEN
access_token_secret=ACCESS_TOKEN_SECRET

class DBListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """


    def on_data(self, data):
        data = json.loads(data)
        pprint.pprint(data['text'])


        return True

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream

            return False

if __name__ == '__main__':
    l = DBListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(languages=['en'], async=True, locations=US)




"""
RETURNED DATA FROM twitter is in the form:
{
    "created_at": "Thu Apr 02 22:16:15 +0000 2015",
    "id": 583754843887571000,
    "id_str": "583754843887570945",
    "text": "Wake up eat watermelon then go to basketball practice",
    "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
    "truncated": false,
    "in_reply_to_status_id": null,
    "in_reply_to_status_id_str": null,
    "in_reply_to_user_id": null,
    "in_reply_to_user_id_str": null,
    "in_reply_to_screen_name": null,
    "user": {
        "id": 2950893090,
        "id_str": "2950893090",
        "name": "Diego Coronado",
        "screen_name": "D_Coronado5",
        "location": "",
        "url": null,
        "description": "gabriela❤️ \njust trying to make it",
        "protected": false,
        "verified": false,
        "followers_count": 99,
        "friends_count": 89,
        "listed_count": 0,
        "favourites_count": 265,
        "statuses_count": 235,
        "created_at": "Mon Dec 29 21:10:03 +0000 2014",
        "utc_offset": null,
        "time_zone": null,
        "geo_enabled": true,
        "lang": "en",
        "contributors_enabled": false,
        "is_translator": false,
        "profile_background_color": "C0DEED",
        "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
        "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
        "profile_background_tile": false,
        "profile_link_color": "0084B4",
        "profile_sidebar_border_color": "C0DEED",
        "profile_sidebar_fill_color": "DDEEF6",
        "profile_text_color": "333333",
        "profile_use_background_image": true,
        "profile_image_url": "http://pbs.twimg.com/profile_images/567430130197229568/p_T9pyJF_normal.jpeg",
        "profile_image_url_https": "https://pbs.twimg.com/profile_images/567430130197229568/p_T9pyJF_normal.jpeg",
        "profile_banner_url": "https://pbs.twimg.com/profile_banners/2950893090/1419888436",
        "default_profile": true,
        "default_profile_image": false,
        "following": null,
        "follow_request_sent": null,
        "notifications": null
    },
    "geo": null,
    "coordinates": null,
    "place": null,
    "contributors": null,
    "retweet_count": 0,
    "favorite_count": 0,
    "entities": {
        "hashtags": [],
        "trends": [],
        "urls": [],
        "user_mentions": [],
        "symbols": []
    },
    "favorited": false,
    "retweeted": false,
    "possibly_sensitive": false,
    "filter_level": "low",
    "lang": "en",
    "timestamp_ms": "1428012975080"
}
"""