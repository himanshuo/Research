from ngram import NGram
from db import DB
from models import User, Tweet, Hashtag

# ngrams = NGram()
mydb = DB()

# ngrams.input_data(mydb)
# ngrams.print_m_most_common_words(100)
# print(ngrams.num_unique_words())
# ngrams.get_synonym_list('take')
# ngrams.num_abbreviations(mydb)

# cd ~/ho2es/Research/twitter/
# source ENV/bin/activate



# There are 2 databases. There is a separate way to get data out of each one.
#
# 1) The mysql database is huge. It has the 17 million tweets.
#    To get data out of it, you have to query it by calling:
#           mydb.get_mysql_data(query)
#    query can be any possible query in mysql.
#    Some query examples include:
#           1) get all tweets:
#               select * from Tweet
#           2) get only 100 Tweets:
#               select * from Tweet limit 100
#           3) get tweets that have over 90 retweets
#               select * from Tweet where Tweet.retweet_count > 90
#           4) get only the text contents of tweets
#               select Tweet.text from Tweet
#           5) get all users
#               select * from User
#           6) get all tweets that have a given user name
#               select * from Tweet, User where Tweet.user_id == User.id and User.name==given_user_name
#
#   http://www.w3schools.com/sql/ is a good reference source/learning resource for database queries.
#   The link is NOT specific for mysql but it is a good resource to understand how to build your custom
#   queries. The syntax for mysql queries are generally the same, but I wouldn't be surprised if you run into
#   a few differences and need to google around a bit.
#   If you need help building a specific query, go ahead and ask me! At one point, I tried to become
#   a query expert. Mixed results. If anything, I know the basics now. I could seriously use a good refresher/challenge.
#
#   The general schema for the mysql database is:
#             Tweet:
#                 id
#                 text
#                 source
#                 user_id
#                 geo
#                 coordinates
#                 place
#                 retweet_count
#                 favorite_count,
#                 timestamp
#             User:
#                 id
#                 name
#                 followers_count
#                 friends_cound
#                 listed_count
#                 favorites_count
#                 statuses_count
#                 created_at
#             HashTag:
#                 id
#                 tag
#             HashTagTweet:
#                 id
#                 hashtag_id
#                 tweet_id
#   The full schema can be found in the schema.sql file.
#
# 2) The sqlite database has only about a 1 million records.
#    To access its contents, you have to do an sqlalchemy query
#    sqlalchemy makes basic objects and you can just get relationships
#    between objects.
#
#    The models (classes) are:
#       Tweet, User, and HashTag
#   their fields are nearly identical to the tables in the mysql schema
#   given above. The full models can be found in the models.py file.
#
#   Some examples of ways to get data out of the sqlite database:
#           1) get all tweets:
#               mydb.session.query(Tweet).all()
#           2) get only 100 Tweets:
#               mydb.session.query(Tweet).limit(100).all()
#           3) get tweets that have over 90 retweets
#               mydb.session.query(Tweet).filter(Tweet.retweet_count > 90).all()
#           4) get only the text contents of tweets
#               mydb.session.query(Tweet.text).all()
#           5) get all users
#               mydb.session.query(User).all()
#           6) get all tweets that have a given user name
#               mydb.session.query(Tweet).filter(Tweet.user.name == given_user_name).all()
#
#
#
# Examples:

# mysql
# mydb.get_mysql_data('select * from tweet limit 10')

# sqlite

# mydb.session.query(Tweet).all()
