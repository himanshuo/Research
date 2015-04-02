__author__ = 'himanshu'
import base64
import requests
import json
from constants import *
import pprint
import urllib.parse.urlencode as percent_encode

def _credentials_to_bearer_token_credentials(API_KEY, API_SECRET):
    """
    converts the credentials from twitter into a new single credentials parameter.
    This new parameter is used when making the initial oauth request to twitter

    base_64_encode(API_KEY:API_SECRET)

    :return: bearer token credential. As byte array.
    """
    k = bytes(API_KEY, "utf-8")
    s = bytes(API_SECRET, "utf-8")
    b = base64.b64encode(k+b":"+s)
    return b.decode("utf-8")

#TESTING _credentials_to_bearer_token_credentials(...)
# t= _credentials_to_bearer_token_credentials("xvz1evFS4wEEPTGEFPHBog","L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg")
# print(t)
# r="eHZ6MWV2RlM0d0VFUFRHRUZQSEJvZzpMOHFxOVBaeVJnNmllS0dFS2hab2xHQzB2SldMdzhpRUo4OERSZHlPZw=="
# print(r)
# print(r==t)


def _create_signature(request_params):
    """
    request_params MUST have:
    oauth_consumer_key	xvz1evFS4wEEPTGEFPHBog
    oauth_nonce	kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg
    oauth_signature_method	HMAC-SHA1
    oauth_timestamp	1318622958
    oauth_token	370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb
    oauth_version	1.0


    :param request_params: values to

    :return:
    """

    collected_params = {}
    for k,v in request_params.items():
        collected_params[percent_encode(k)] = [percent_encode(v)]
    sorted(collected_params)





def get_token(TOKEN_URL, CONSUMER_KEY, ):
    """
    THIS IS HOW THE REQUEST LOOKS:

    POST /oauth2/token HTTP/1.1
    Host: api.twitter.com
    User-Agent: My Twitter App v1.0.23
    Authorization: Basic eHZ6MWV2RlM0d0VFUFRHRUZQSEJvZzpMOHFxOVBaeVJn
                         NmllS0dFS2hab2xHQzB2SldMdzhpRUo4OERSZHlPZw==Content-Type: application/x-www-form-urlencoded;charset=UTF-8
    Content-Length: 29
    Accept-Encoding: gzip

    grant_type=client_credentials


    CURL:
     curl --get 'https://stream.twitter.com/1.1/statuses/filter.json'
     --data 'track=twitter'
     --header
        'Authorization: OAuth oauth_consumer_key="lmuKdHdhB1OgEmVaQuiU3EBSL",
        oauth_nonce="b37ca4d1385549271eecd03bb04a507a",
        oauth_signature="ru5YqvHK7a33Pu3O2zNcxNZQzKU%3D",
        oauth_signature_method="HMAC-SHA1",
        oauth_timestamp="1428008673",
        oauth_token="208686751-zEEyTAJOBKFLxwnxyH9cHTeIjrcpzyZWq4RTU0Ty",
        oauth_version="1.0"' --verbose

    :return:
    """




    headers = {
        "Authorization": build_authorization_string(CONSUMER_KEY, )
    }




    data = json.dumps({
        #"grant_type" : "client_credentials"
        "track":"twitter"
    })
    #print(data)

    r = requests.post(TOKEN_URL, headers=headers, data=data)
    pprint.pprint(r.json())


t = _credentials_to_bearer_token_credentials(API_KEY, API_SECRET)
get_token(TOKEN_URL, t)
