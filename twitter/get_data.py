from __future__ import absolute_import, print_function
from constants import *
#During setup, make sure to install CUSTOM version of Tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from db import DB
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

        self.db = DB()

        pass



    def on_data(self, data):
        data = json.loads(data)

        if 'limit' in data and 'track' in data['limit']:
            return True # ignore current, continue to next tweet.





        # pprint.pprint(data['text'])
        #print('.',end="", flush=True)


        if 'delete' in data and data['delete']:
            return True #ignore deleted tweets.

        if 'text' in data:
             self.db.add_twitter_data(twitter_data=data)




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

    def on_exception(self, exception):
        """Called when an unhandled exception occurs."""
        message= str(exception)
        message = message + "\n" + "The python script broke. Go check it out."
        self.send_emails(title="EXCEPTION", content=message)
        return



    def send_emails(self, title, content):

        try:
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
        except:
            print("-----------------ERROR. EMAIL WAS NOT SENT------------------")
            print(title)
            print(content)













if __name__ == '__main__':
    l = DBListener()

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    try:

        stream = Stream(auth, l)
        stream.filter(languages=['en'], async=True, locations=US, stall_warnings=True)

    except:
        l.send_emails(title="Python Script Failed", content="Python Script Failed. Must Manually Restart Script.")




