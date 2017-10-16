
# coding: utf-8

# In[6]:

from __future__ import unicode_literals
import re
from textblob import TextBlob
import twitter


# In[8]:

def get_tweet_sentiment(tweet):
       
        analysis = TextBlob(clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


# In[9]:

def clean_tweet(tweet):

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# In[11]:

def tor(final):

    total = len(final)
    total = float(total)

    pos = 0.0
    neg = 0.0
    neu = 0.0

    for tweet in final:
        bclear = tweet.text
        aclear = clean_tweet(bclear)
        ablob = TextBlob(aclear)
        sent = ablob.sentiment.polarity
        if(sent > 0):
            pos = pos+1
        elif(sent == 0):
            neu = neu+1
        else:
            neg = neg+1
    
    if total > 0:
        posper = pos/total*100
        negper = neg/total*100
        neuper = neu/total*100
        polar = [posper,negper,neuper]
    else:
        polar = [0, 0, 0]
    
    return(polar)


# In[12]:



def getRes(query, keys):

    a = []
        
    s = "q="+query
    api = twitter.Api(consumer_key=keys['consumer_key'],
        consumer_secret=keys['consumer_secret'],
        access_token_key=keys['access_token'],
        access_token_secret=keys['access_token_secret']
    )
    print (api)
    final = api.GetSearch(raw_query=s)
    a = tor(final)

    return a
        


def getSentimentGraph (query, keys):

    # calculate


    r = getRes(query, keys)
    res = [
        ['Handle'.encode('utf-8'), 'Positive'.encode('utf-8'), 'Negative'.encode('utf-8'), 'Neutral'.encode('utf-8')]
    ]
    res = [
        ["Sentiment".encode('utf-8'), "Number".encode('utf-8')],
        ["Positive".encode('utf-8'), r[0]],
        ["Negative".encode('utf-8'), r[1]],
        ["Neutral".encode('utf-8'), r[2]],
    ]

    return res


