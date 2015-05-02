from __future__ import absolute_import, print_function
from constants import *
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import time
import sendgrid
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


    def on_connect(self):
        """Called once connected to streaming server.
        This will be invoked once a successful response
        is received from the server. Allows the listener
        to perform some work prior to entering the read loop.
        """

        #todo: set up connection to database here. OR do it at toplevel.

        pass

    def _stream_to_db_format(self, raw_data):
        #todo: convert from raw_data to db format
        pass

    def on_data(self, data):
        data = json.loads(data)
        # pprint.pprint(data['text'])

        #todo: make db format
        #todo: add to db



        if 'warning' in data:
            self.on_warning(data['warning'])

        return True

    def on_error(self, status_code):

        if status_code == 420: #Rate Limited (too many login attempts)
            #returning False in on_data disconnects the stream

            self.send_emails(  title="BROKEN. STATUS CODE == 420",
                               content="BROKEN. STATUS CODE == 420. Rate Limited (too many login attempts) ")

            return False


        return False


    def on_warning(self, warning):
        if warning.get("percent_full", 0) > 80:
            email_message = "percent_full exceeded 80% ( percent_full = %d ) so temporarily stopping stream." % warning.get("percent_full",0)
            email_message += "\n"
            email_message += warning.get('message','')

            self.send_emails(  title=warning.get('code','WARNING'),
                               content=email_message)
            return False



    def send_emails(self, title, content):

        sg_username = SG_USERNAME
        sg_password = SG_PASS

        sg = sendgrid.SendGridClient(sg_username, sg_password)
        message = sendgrid.Mail()


        message.set_from(FROM_EMAIL)
        message.set_subject(title)
        message.set_text(content)
        for email in EMAIL_TO:
            message.add_to(email)


        sg.send(message)













if __name__ == '__main__':
    l = DBListener()
    import pdb;pdb.set_trace()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    try:
        stream = Stream(auth, l)
        stream.filter(languages=['en'], async=True, locations=US, stall_warnings=True)
    except:
        l.send_emails(title="Python Script Failed", content="Python Script Failed. Must Manually Restart Script.")




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





"""
ERROR CODES THAT TWITTER SENDS:

Code	Name	Description
1	Shutdown	The feed was shutdown (possibly a machine restart)
2	Duplicate stream	The same endpoint was connected too many times.
3	Control request	Control streams was used to close a stream (applies to sitestreams).
4	Stall	The client was reading too slowly and was disconnected by the server.
5	Normal	The client appeared to have initiated a disconnect.
6	Token revoked	An oauth token was revoked for a user (applies to site and userstreams).
7	Admin logout	The same credentials were used to connect a new stream and the oldest was disconnected.
8		Reserved for internal use. Will not be delivered to external clients.
9	Max message limit	The stream connected with a negative count parameter and was disconnected after all backfill was delivered.
10	Stream exception	An internal issue disconnected the stream.
11	Broker stall	An internal issue disconnected the stream.
12	Shed load	The host the stream was connected to became overloaded and streams were disconnected to balance load. Reconnect as usual.
"""


"""
STALL WARNINGS ARE USEFUL. ENABLE THEM.

Stall warnings (warning)
When connected to a stream using the stall_warnings parameter, you may receive status notices indicating the current health of the connection. See the stall_warnings documentation for more information.

{
  "warning":{
    "code":"FALLING_BEHIND",
    "message":"Your connection is falling behind and messages are being queued for delivery to you. Your queue is now over 60% full. You will be disconnected when the queue is full.",
    "percent_full": 60
  }
}
Note that in the case of Site Streams warning messages apply to the entire stream and will not be wrapped with a for_user envelope.


"""



"""
STATUS CODES TO CHECK FOR:
https://dev.twitter.com/streaming/overview/connecting
"""