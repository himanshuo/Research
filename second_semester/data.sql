-- to set up database, use command:
--                    sqlite3 second.db < data.sql

CREATE TABLE Hashtag(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
hashtag TEXT,
checked BOOLEAN, -- checked = once you scrape a hashtag, you dont scrape it again
ref BIGINT); -- number of times this hashtag has been referenced


CREATE TABLE Tweet(
tweetid INTEGER PRIMARY KEY,
username INTEGER,
text TEXT,
retweet_count INTEGER,
favorite_count INTEGER,
twitterID BIGINT,
created_at TEXT, -- this is created using alter table
FOREIGN KEY(username) REFERENCES Username(userid)
);



CREATE TABLE Username(
userid INTEGER PRIMARY KEY,
follower_count INTEGER,
username varchar(30),
checked BOOLEAN,
ref BIGINT);



CREATE TABLE SpecialWord(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  word VARCHAR(30),
  checked BOOLEAN,
  ref BIGINT
);

CREATE TABLE FullVector(
  tweet_id INTEGER PRIMARY KEY,
  full_vector TEXT
);

-- ALTER TABLE Tweet ADD COLUMN created_at TEXT;
