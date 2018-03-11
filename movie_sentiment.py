# Dependencies
import json
from pprint import pprint
from datetime import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import (consumer_key, consumer_secret,
                    access_token, access_token_secret)

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

search_term = "Black Panther"

public_tweets = api.search(search_term,
                           count=25,
                           until="2018-03-02")

public_tweets

# for tweet in public_tweets['statuses']:
#     print(tweet['text'])
#     print(tweet['created_at'])
# Target user
search_term = "Black Panther"

# Create variable for holding the oldest tweet
oldest_tweet = None

# Create list of dictionaries
sentiment = []

# Get all tweets from home feed (for each page specified)
public_tweets = api.search(search_term,
                           count=25,
                           lang='en',
                           result_type="recent",
                           until="2018-03-01",
                           max_id=oldest_tweet)

# Loop through all tweets
for tweet in public_tweets['statuses']:

    # Grab tweet data
    name = tweet['user']['screen_name']
    tweet_text = tweet['text']
    date = tweet['created_at']

    # Run Vader Analysis on each tweet
    results = analyzer.polarity_scores(tweet["text"])
    compound = results["compound"]
    positive = results['pos']
    neutral = results['neu']
    negative = results['neg']

    # Create dictionary holding tweet data
    tweet_dict = {'Handle': name, 'Tweet': tweet_text, 'Date': date, 'Compound': compound,
                  'Positive': positive, 'Neutral': neutral, 'Negative': negative}

    # Append tweet data to sentiment list
    sentiment.append(tweet_dict)

    # Reassign the the oldest tweet (i.e. the max_id)
    oldest_tweet = int(tweet["id_str"])

    # Subtract 1 so the previous oldest isn't included
    # in the new search
    oldest_tweet = oldest_tweet - 1

pprint(sentiment)
