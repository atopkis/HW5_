from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk
nltk.download('punkt')
#Could not get punkt to download

# uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time: Mon 5:30-7
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)

#Code for OAuth ends

#Write your code below:

f_name = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}



def make_request_using_cache(baseurl, params={'screen_name':username,'count':num_tweets}):
    unique_ident = (baseurl, params)

    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]

    else:
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        tw = open(twitter_cache,"w")
        tw.write(dumped_json_cache)
        tw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this

#Code for Part 1:Get Tweets
baseurl='https://api.twitter.com/1.1/statuses/user_timeline.json'
params={'screen_name':username,'count':num_tweets}
r=requests.get(baseurl, params=params, auth=auth)
json_twit=json.loads(r.text)
#f_name=open('tweet.json', 'w')
#f_name.write(json.dumps(json_twit, indent=4))
#f_name.close()
#Code for Part 2:Analyze Tweets


tweet=[]
for c in json_twit:
    tweet.append(c['text'])

big_string=' '.join(tweet)





tokens = nltk.word_tokenize(big_string)
freqDist = nltk.FreqDist(token for token in tokens if token.isalpha() and not 'http' or 'https' or 'RT')
for word, frequency in freqDist.most_common(10):
    print(word + " " + str(frequency))


if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
