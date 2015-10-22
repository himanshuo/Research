import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import wordnet as wn
from pprint import pprint
import re
class NGram(object):

    def __init__(self):
        self.tokens = {}  # {word -> freq}


    """
    https://www.ibm.com/developerworks/community/blogs/nlp/entry/tokenization?lang=en


    things to think about when tokenizing:
    1) ignore lowercase/uppercase
    2) remove ' * "" ~`! and other punctuation
    3) periods can refer to end of sentences OR to abbreviations.
    4) how do these specific tokenization things affect my specific twitter data
    5) it looks like you are supposed to train the punkt module within nltk package using your own test corpus
    6) about 400k tokens in training corpora
    7) HOWEVER, for word tokenizer, nltk already has a word_tokenize function which uses TreeBank corpa to already tokenize
    8) TreebankWordTokenizer: (“this’s a test”) -> [‘this’, “‘s”, ‘a’, ‘test’]
    alternatives to TreebankWordTokenizer are: PunktWordTokenizer and WordPunktTokenizer
    9) PunktWordTokenizer: splits on punctuation, but keeps it with the word
    10) for example, "this's a test" -> [‘this’, “‘s”, ‘a’, ‘test’]
    11) WordPunctTokenizer: splits all punctuations into seperate tokens.
    12) for example: (“This’s a test”) -> [‘This’, “‘”, ‘s’, ‘a’, ‘test’]



    BEST THING FOR US: nltk.tokenize.casual.TweetTokenizer is specifically for Twitter
    class nltk.tokenize.casual.TweetTokenizer(preserve_case=True, reduce_len=False, strip_handles=False)
    preserve_case: turns everything but emoticons into lowercase
    reduce_len: makes it so that if 3 chars or more are repeated, then we turn them into just 3 chars: "himhimhimhim" -> "him"
    strip_handles: remove twitter handles

    HOW TweetTokenizer works:
        tuple regex_strings defines a list of regular expression strings.   USES regex
        regex_strings strings are put, in order, into a compiled regular expression object called word_re.
        tokenization is done by word_re.findall(s), where s is the user-supplied string, inside the tokenize() method of the class Tokenizer.
        When instantiating Tokenizer objects, there is a single option: preserve_case. By default, it is set to True. If it is set to False, then the tokenizer will downcase everything except for emoticons.


    WHAT are the regex_strings regex expressions (don't understand the specifics of each regex):
        WORD_RE = re.compile(r"(%s)" % "|".join(REGEXPS), re.VERBOSE | re.I
                         | re.UNICODE)

        # The emoticon string gets its own regex so that we can preserve case for
        # them as needed:
        EMOTICON_RE = re.compile(EMOTICONS, re.VERBOSE | re.I | re.UNICODE)

        # These are for regularizing HTML entities to Unicode:
        ENT_RE = re.compile(r'&(#?(x?))([^&;\s]+);')




    proper nouns increases popularity
        -proper nouns = upper case
    TOKENIZATION STEPS:
    1)upper/lower case -> all caps might get more SO we will NOT ignore case.
    2)white space word seperation
    3)strip_handles = TRUE
    4)for abbreviations, we want to remove them from original tweet. put them in tokens_list. and then use tokenize()
        determine how frequently periods are used by going through tweets.
        num periods per tweet. get avg.  if 1-> sentence ending period. if 2/3/more -> abbreviation.
        INSTEAD OF THE ABOVE, we should go through and check is r" "
    5) hyphenated words. Keep them. Toolkit automatically keeps them.
    6) figure out how to handle URL's ******* NOT DONE *******




    RETWEET could be because of a link. SO, content of tweet doesnt matter. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    have benchmarks for minimal vialibitly of tweet. With new subset, we normalize.
    This is to gauge relative success of tweet.


    To determine if we should consider abbreviations as 1 word, we checked how frequently abbreviations are used in tweets.
    We got 3240 abbreviations in 559157 tweets. We looked through the data, and lots of "abbreviations" are incorrect spacing
     by users. For example " I hate you.Gosh,"
    Looking through the tweets, we estimate only about 1000 of the tweets have abbreviations. Therefore, checking for abbreviations
    seems not necessary.


    """

    def get_synonym_list(self, word):
        """
        NEED TO LOOK AT POS (part of speech) tagging. this is in nltk.
        :param word:
        :return:
        """
        synomyns = {}
        ssets = wn.synsets(word)
        for sset in ssets:
            for lemma in sset.lemmas():
                synomyns[str(lemma.name())] = self.tokens[str(lemma.name())] if str(lemma.name()) in self.tokens else 0

        pprint(synomyns)

    def input_data(self, db):
        """

        :param db: general connection to database. REQUIRES db.tweets() to give you a iterable of tweets as text.
        :output: puts {word: num_occurences_of_word} into self.tokens
        """
        num_errors = 0
        limit = 100
        tknizer = TweetTokenizer(strip_handles=True)
        for tweet in db.tweets():
            try:
                words = tknizer.tokenize(tweet)

                for word in words:
                    if word in self.tokens:
                        self.tokens[word] += 1
                    else:
                        self.tokens[word] = 1
                limit -= 1
                if limit<0:
                    break
            except TypeError:

                num_errors += 1
                if num_errors >10:
                    pprint(self.tokens)
                    break


    def print_m_most_common_words(self, m):
        sorted_list = sorted(self.tokens.items(), key=lambda x: x[1])

        for k,v in reversed(sorted_list):
            print(k,v)
            m -= 1
            if m<=0:
                break


    def num_unique_words(self):
        return len(self.tokens)

    def num_abbreviations(self, db):
        REGEX = r"[a-zA-Z](\.[a-zA-Z])+(\.){0,1}"
        pattern = re.compile(REGEX)

        num_matches = 0
        num_errors = 0
        num_tweets = 0
        for tweet in db.tweets():
            try:
                res = pattern.search(tweet.split('http')[0])
                if res:
                    num_matches += 1
                    print(tweet)
                num_tweets += 1

            except TypeError:

                num_errors += 1
                if num_errors >10:
                    pprint(self.tokens)
                    break

        pprint(num_matches)
        pprint(num_tweets)


