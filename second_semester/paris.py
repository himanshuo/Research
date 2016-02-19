import sqlite3
import nltk
import os
import json
import time
import operator
import random
import math
import sys
import functions
import unigrammodel
from TwitterSearch import *
import signal
import subprocess

tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()

retweet_count_threshold = 0
follower_count_threshold = 0
content_threshold = 0

ts1 = TwitterSearch(
    consumer_key = 'ZMXcgM8WlfUORmmoeydccmJhK',
    consumer_secret = 'wfKVxQEme1TaS0INiry4DPTQmk8RVhZlwEExAMWPjXisi2okeD',
    access_token = '4570126217-OXHGBYKXbiGmoJzwmehx4mB73u7qmoL8OU7gSF7',
    access_token_secret = 'IZhl0zqDUtOmn2BPSAenw3xMgJ1EVaXSmbSGyWF2QOqYv'
)

stopwords = ['i','to','the','a','and','in','you','my','of','it','for','is','on','that','this','me']
punctuations = ['``',':','!','.',',','&','(',')','*','^','%','$','#','@','~','""',';','<','>','/','?','...','-']

conn2 = sqlite3.connect('new_tweets.db')
c2 = conn2.cursor()

last_tweets = 0
last_total_hashs = 0
last_done_hashs = 0
last_total_users = 0
last_done_users = 0

pro = subprocess.Popen("python scrape_new.py", stdout=subprocess.PIPE,
                       shell=True, preexec_fn=os.setsid)

out_file = open("results_log.txt","a")
while True:
    count = 0
    print "UPDATE:"
    print time.strftime("%Y-%m-%d %H:%M")
    print ""
    out_file.write("UPDATE:\n" + str(time.strftime("%Y-%m-%d %H:%M")) + "\n\n")
    total_tags = c2.execute("SELECT count(*) from Hashtag;")
    for i in total_tags:
        print "Total Hashtags in DB: " + str(i[0]) + ", " + str(int(i[0]) - last_total_hashs) + " in the last 3 minutes"
        out_file.write("Total Hashtags in DB: " + str(i[0]) + ", " + str(int(i[0]) - last_total_hashs) + " in the last 3 minutes\n")
        count += int(i[0]) - last_total_hashs
        last_total_hashs = int(i[0])

    done_tags = c2.execute("SELECT count(*) from Hashtag where checked == 1;")
    for i in done_tags:
        print "Total Hashes checked: " + str(i[0]) + ", " + str(int(i[0]) - last_done_hashs) + " in the last 3 minutes"
        out_file.write("Total Hashes checked: " + str(i[0]) + ", " + str(int(i[0]) - last_done_hashs) + " in the last 3 minutes\n")
        count += int(i[0]) - last_done_hashs
        last_done_hashs = int(i[0])

    total_tweets = c2.execute("SELECT count(*) from Tweet;")
    for i in total_tweets:
        print "Total Tweets in DB: " + str(i[0]) + ", " + str(int(i[0]) - last_tweets) + " in the last 3 minutes"
        out_file.write("Total Tweets in DB: " + str(i[0]) + ", " + str(int(i[0]) - last_tweets) + " in the last 3 minutes\n")
        count += int(i[0]) - last_tweets
        last_tweets = int(i[0])

    total_users = c2.execute("SELECT count(*) from Username;")
    for i in total_users:
        print "Total Users in DB: " + str(i[0]) + ", " + str(int(i[0]) - last_total_users) + " in the last 3 minutes"
        out_file.write("Total Users in DB: " + str(i[0]) + ", " + str(int(i[0]) - last_total_users) + " in the last 3 minutes\n")
        count += int(i[0]) - last_total_users
        last_total_users = int(i[0])

    done_users = c2.execute("SELECT count(*) from Username where checked == 1;")
    for i in done_users:
        print "Total Users Checked: " + str(i[0]) + ", " + str(int(i[0]) - last_done_users) + " in the last 3 minutes"
        out_file.write("Total Users Checked: " + str(i[0]) + ", " + str(int(i[0]) - last_done_users) + " in the last 3 minutes\n")
        count += int(i[0]) - last_done_users
        last_done_users = int(i[0])
    print "count: " + str(count)
    print "\n"

    if count < 1:
        print "restarting the process"
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
        time.sleep(10)
        pro = subprocess.Popen("python scrape_new.py", stdout=subprocess.PIPE,
                               shell=True, preexec_fn=os.setsid)
        print "succesfully restarted the process"

    time.sleep(180)
