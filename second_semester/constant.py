# from TwitterSearch import *
# filtered out
stopwords = ['i','to','the','a','and','in','you','my','of','it','for','is','on','that','this','me']
punctuations = ['``',':','!','.',',','&','(',')','*','^','%','$','#','@','~','""',';','<','>','/','?','...','-']
seed_hashtags = ["election2016","trump","clinton","sanders","cruz","rubio","kasich","gopdebate","demdebate"]

retweet_count_threshold = 10 # atleast 10 retweets
follower_count_threshold = 100 # atleast 100 followers
content_threshold = 10  # atleast 10 remaining content words (after filtering)
hashtag_ref_threshold = 10
user_ref_threshold = 0
word_ref_threshold = 10
tweet_time_difference_threshold = 2 # closer to 0 is MORE restrictive
tweet_follower_difference_threshold = 1.5 # closer to 1 is MORE restrictive, less than 1 is impossible

# Unigram model things

unigram_stopwords = ['a', "a's", 'able', 'about', 'above', 'according', 'accordingly', 'across', 'actually', 'after',
    'afterwards', 'again', 'against', "ain't", 'all', 'allow', 'allows', 'almost', 'alone', 'along', 'already', 'also',
    'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 'anyone', 'anything',
    'anyway', 'anyways', 'anywhere', 'apart', 'appear', 'appreciate', 'appropriate', 'are', "aren't", 'around', 'as', 'aside',
    'ask', 'asking', 'associated', 'at', 'available', 'away', 'awfully', 'b', 'be', 'became', 'because', 'become', 'becomes',
    'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'best', 'better',
    'between', 'beyond', 'both', 'brief', 'but', 'by', 'c', "c'mon", "c's", 'came', 'can', "can't", 'cannot', 'cant', 'cause',
    'causes', 'certain', 'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently',
    'consider', 'considering', 'contain', 'containing', 'contains', 'corresponding', 'could', "couldn't", 'course', 'currently',
    'd', 'definitely', 'described', 'despite', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', "don't",
    'done', 'down', 'downwards', 'during', 'e', 'each', 'edu', 'eg', 'eight', 'either', 'else', 'elsewhere', 'enough',
    'entirely', 'especially', 'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere',
    'ex', 'exactly', 'example', 'except', 'f', 'far', 'few', 'fifth', 'first', 'five', 'followed', 'following', 'follows',
    'for', 'former', 'formerly', 'forth', 'four', 'from', 'further', 'furthermore', 'g', 'get', 'gets', 'getting', 'given',
    'gives', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'h', 'had', "hadn't", 'happens', 'hardly', 'has',
    "hasn't", 'have', "haven't", 'having', 'he', "he's", 'hello', 'help', 'hence', 'her', 'here', "here's", 'hereafter', 'hereby',
    'herein', 'hereupon', 'hers', 'herself', 'hi', 'him', 'himself', 'his', 'hither', 'hopefully', 'how', 'howbeit', 'however', 'i',
    "i'd", "i'll", "i'm", "i've", 'ie', 'if', 'ignored', 'immediate', 'in', 'inasmuch', 'inc', 'indeed', 'indicate', 'indicated',
    'indicates', 'inner', 'insofar', 'instead', 'into', 'inward', 'is', "isn't", 'it', "it'd", "it'll", "it's", 'its', 'itself', 'j',
    'just', 'k', 'keep', 'keeps', 'kept', 'know', 'knows', 'known', 'l', 'last', 'lately', 'later', 'latter', 'latterly', 'least',
    'less', 'lest', 'let', "let's", 'like', 'liked', 'likely', 'little', 'look', 'looking', 'looks', 'ltd', 'm', 'mainly', 'many',
    'may', 'maybe', 'me', 'mean', 'meanwhile', 'merely', 'might', 'more', 'moreover', 'most', 'mostly', 'much', 'must', 'my',
    'myself', 'n', 'name', 'namely', 'nd', 'near', 'nearly', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new',
    'next', 'nine', 'no', 'nobody', 'non', 'none', 'noone', 'nor', 'normally', 'not', 'nothing', 'novel', 'now', 'nowhere', 'o',
    'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others',
    'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own', 'p', 'particular', 'particularly',
    'per', 'perhaps', 'placed', 'please', 'plus', 'possible', 'presumably', 'probably', 'provides', 'q', 'que', 'quite', 'qv', 'r', 'rather',
    'rd', 're', 'really', 'reasonably', 'regarding', 'regardless', 'regards', 'relatively', 'respectively', 'right', 's', 'said',
    'same', 'saw', 'say', 'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self',
    'selves', 'sensible', 'sent', 'serious', 'seriously', 'seven', 'several', 'shall', 'she', 'should', "shouldn't", 'since', 'six',
    'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry',
    'specified', 'specify', 'specifying', 'still', 'sub', 'such', 'sup', 'sure', 't', "t's", 'take', 'taken', 'tell', 'tends', 'th',
    'than', 'thank', 'thanks', 'thanx', 'that', "that's", 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence',
    'there', "there's", 'thereafter', 'thereby', 'therefore', 'therein', 'theres', 'thereupon', 'these', 'they', "they'd", "they'll",
    "they're", "they've", 'think', 'third', 'this', 'thorough', 'thoroughly', 'those', 'though', 'three', 'through', 'throughout',
    'thru', 'thus', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'twice', 'two',
    'u', 'un', 'under', 'unfortunately', 'unless', 'unlikely', 'until', 'unto', 'up', 'upon', 'us', 'use', 'used', 'useful', 'uses',
    'using', 'usually', 'uucp', 'v', 'value', 'various', 'very', 'via', 'viz', 'vs', 'w', 'want', 'wants', 'was', "wasn't", 'way',
    'we', "we'd", "we'll", "we're", "we've", 'welcome', 'well', 'went', 'were', "weren't", 'what', "what's", 'whatever', 'when',
    'whence', 'whenever', 'where', "where's", 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether',
    'which', 'while', 'whither', 'who', "who's", 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'willing', 'wish', 'with',
    'within', 'without', "won't", 'wonder', 'would', 'would', "wouldn't", 'x', 'y', 'yes', 'yet', 'you', "you'd", "you'll", "you're",
    "you've", 'your', 'yours', 'yourself', 'yourselves', 'z', 'zero']

unigram_threshold = 0.0
unigram_punctuations = [u'\\',u'}',u'@',u'+',u'$',u']',u':',u',',u'^',u';',u'-',u'&',u'%',u'{',u'_',u'.',u'\'',u'|',u'`',u'=',u'/',u'(',u'!',u')',u'~',u'[',u'?',u'*',u'#']

# keys
#
# ts1 = TwitterSearch(
#     consumer_key = 'nr2GFw3XVpNOSD9ZOlddfhGxq',
#     consumer_secret = 'UCv6lKJXjRJyIvtOYdSoIBWzusfp4Iy6zAE5UGAM8dhEk8Svp8',
#     access_token = '4549049355-hpKIheHy9JGVRrDnsCv6iF7Sf2EoHglbnJTl9Y3',
#     access_token_secret = 'oWMgAgzW0RMyx94jSrMoJxDrSOZPvUHykvs8M2dDHWjMw'
# )
#
# ts2 = TwitterSearch(
#     consumer_key = 'bIblpmxgiTBOgmsDtSyEkj79f',
#     consumer_secret = 'XWQs98ZIBBuD1hJ0wuHRNfWw9f5SjDplyYdljQqZ57onXkNQqK',
#     access_token = '4549049355-NRCTfBlktXDb9H0ENsOZVj3YZrBWVbVvIRRv6yr',
#     access_token_secret = 'RRH8ksVn6McAXoChh6Z6PYgyS2mHA7tcCxX1JPV7t77Dc'
# )
#
# ts3 = TwitterSearch(
#     consumer_key = 'LmKNKUYpwgmdKzu2KsBhHk5zn',
#     consumer_secret = '3wcePG0IDwtfNMXt1mbs4DZK3xfv28DVxarmsK8mzlC7HBbN3B',
#     access_token = '4549049355-TF4DjiXRjl6buXcQWREpYMuGGNe6ceY3up1aREo',
#     access_token_secret = 'F7hHW7Q0uMPMMloaP4l4J3vAjDyNnvtiFsNCJ86Z2dYm9'
# )
#
# ts4 = TwitterSearch(
#     consumer_key = 'vUPxVFAtrLtKicCTLdKebmtMz',
#     consumer_secret = 'jNztwiJJsXMpK1n7zIpajTZVp4q2pvdLuCJZ0PUVXpmvubv1Qr',
#     access_token = '4549049355-xEg0t50dljrofN9jGOaJZITKsqqO9dTMVhafAfZ',
#     access_token_secret = 'wnH6gjWxMcso9y3H7kJoGIOPHA1LlKuQfl3TSa1sGonJB'
# )
#
# ts5 = TwitterSearch(
#     consumer_key = 'Uyh9UjqNLI85SPcFWj83yYgCk',
#     consumer_secret = 'snvA1xYmpayuXcDwavEAjnnockIyRBo7cMSdO8EbvRwmBQCKDg',
#     access_token = '4569957028-E9qX8y96tKFS9ylK58E1raUU5j5Z6aP5rcoouGH',
#     access_token_secret = 'sCr2f3YaZfZF42nIfnVLSEPV0Tkbru3fiNAWdDHyQzURQ'
# )
#
# ts6 = TwitterSearch(
#     consumer_key = 'tpqNFMMlg2MuHW70EJBC1bJ9A',
#     consumer_secret = 'LBPhWbGolH4ohQfyCcAnPLSBx4fklksyerhUGSqiHOeEdU8jFO',
#     access_token = '4569957028-5Fy3y1pdT2OBHYriYK1W1w3UPlqou1e7TPqqpGG',
#     access_token_secret = 'eUQQGaeXjoO2hlp1XGXGDRB8yBKBsszfUusJbFFrRLbUk'
# )
#
# ts7 = TwitterSearch(
#     consumer_key = 'W85OOlizRjcIaFwLG6XpC9u2v',
#     consumer_secret = '9AJKgaqNXK8tHhPEEHOe8BFk82B2JhVtOCXlrFDf8b5mDIfpwV',
#     access_token = '4569957028-YE6dRXp4KcVvy2rskN8WtL3ojVqhyHVJwhHZgLu',
#     access_token_secret = '5DoMvgRo21LHm4HRtJqMQ8evs756umfcdKzRQJThr8FWO'
# )
#
# ts8 = TwitterSearch(
#     consumer_key = '2I6HK4aRWuYhSNENiH487VRhk',
#     consumer_secret = 'sW3zBQLSHcuc32AcWQUdFpwRWFel7X2siR55v3FE62hz5hNNsm',
#     access_token = '4569931877-OLHVuav8XmHsHdRh3RUGI5zdrjlLFVwrliIxkJk',
#     access_token_secret = '8qspicVCzhdFeA9Plq6lGjubBEnINM0AqPS3i2jDwe93h'
# )
#
# ts9 = TwitterSearch(
#     consumer_key = 'Oa89wcEJzsqVJ7CGLINzYJY6o',
#     consumer_secret = 'QtkHjT4g7WwSHlhbqyBmDuSbpxR46TCVLSfgXSICpB74mCu9ek',
#     access_token = '4569931877-tmLgt1pAXAMx4IWkSXOYMORElxN72qar4p2j22B',
#     access_token_secret = 'XeP9knsl4iuwvTWg4OuhTISXSaqpbN5s8UKwYrA0TQj7B'
# )
#
# ts10 = TwitterSearch(
#     consumer_key = 'Yf6df4Awqpt44UL7mxxK0avLP',
#     consumer_secret = 'EUHH9qXDLi3PGaBEHSXDqWxlHmFJ3K8733skzNFCjtqaC0q2Q6',
#     access_token = '4569931877-s6D15iiRI1OaQYoRI8HCh2KUpE0Q1eqC8NZF3sf',
#     access_token_secret = 'qtBIKYd7bnQcsMslEaqpXXEkSUvAJg3TlBgPbEvVA1Czf'
# )
