import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data','twitter.db')
engine = create_engine('sqlite:///{}'.format(FILE_PATH), echo=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    screen_name = Column(String)
    location = Column(String)
    followers = Column(Integer)
    friends = Column(Integer)
    favorites = Column(Integer)
    statuses = Column(Integer)
    created_at = Column(DateTime)

    tweets = relationship("Tweet", backref=backref('user'))

class Tweet(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    text = Column(String)


    geo = Column(String)
    coordinates = Column(String)
    place = Column(String)

    retweet_count = Column(Integer)
    favorite_count = Column(Integer)

    user_id = Column(Integer, ForeignKey('user.id'))
    hashtags = relationship('Hashtag', backref=backref('tweet'))


class Hashtag(Base):
    __tablename__ = 'hashtag'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    tweet_id = Column(Integer, ForeignKey('tweet.id'))

Base.metadata.create_all(engine)
