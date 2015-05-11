CREATE TABLE Tweet (
id SERIAL, /* SERIAL is an alias for BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE */
text VARCHAR(160) NOT NULL,
source VARCHAR(800),
user_id BIGINT REFERENCES User(id),
geo VARCHAR(800),
coordinates VARCHAR(800),
place VARCHAR(800),
retweet_count INT,
favorite_count INT,
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE User (
id SERIAL,
name VARCHAR(160),
followers_count INT,
friends_count INT,
listed_count INT,
favorites_count INT,
statuses_count INT,
created_at TIMESTAMP DEFAULT 0
);

CREATE TABLE HashTag (
id SERIAL,
tag VARCHAR(160) UNIQUE
);

CREATE TABLE HashTagTweet(
id SERIAL,
hashtag_id BIGINT REFERENCES HashTags(id),
tweet_id BIGINT REFERENCES Tweet(id)
);


/*
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
*/