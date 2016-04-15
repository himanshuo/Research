import random

data = open('all_tweets.data', 'r').read().split('\n')
test = open('test.data', 'w')
train = open('train.data', 'w')

test_str = ""
train_str = ""
for line in data:

    if random.random() < 0.2:
        test_str += line + "\n"
    else:
        train_str += line + "\n"

test_str = test_str[:-1]
train_str = train_str[:-1]
test.write(test_str)
train.write(train_str)
test.close()
train.close()
