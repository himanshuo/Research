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


-- ALTER TABLE Tweet ADD COLUMN created_at TEXT;
