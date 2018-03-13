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
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser(),
                 wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Target user
search_term = "a wrinkle in time"

# Create variable for holding the oldest tweet
oldest_tweet = None

# Create list of dictionaries
sentiment = []

# "Real Person" Filters
min_tweets = 5
max_tweets = 10000
max_followers = 2500
max_following = 2500
lang = "en"

# Date
search_date = "2018-03-08"

# Loop through 500 times (total of 500000 tweets)
for x in range(500):

    # Get all tweets from home feed (for each page specified)
    public_tweets = api.search(search_term,
                               count=1000,
                               lang='en',
                               until=search_date,
                               max_id=oldest_tweet)

    # Loop through all tweets
    for tweet in public_tweets['statuses']:

        # Use filters to check if user meets conditions
        if (tweet["user"]["followers_count"] < max_followers and
            tweet["user"]["statuses_count"] > min_tweets and
            tweet["user"]["statuses_count"] < max_tweets and
            tweet["user"]["friends_count"] < max_following and
                tweet["user"]["lang"] == lang):

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

# Create dataframe
awit_tweets = pd.DataFrame(sentiment)

# Reorder columns
awit_tweets = awit_tweets.iloc[:, [2, 6, 1, 0, 5, 4, 3]]

# Save to csv
awit_tweets.to_csv(f'sent_data/{search_date}_AWIT_sentiment.csv', encoding='utf-8', index=False)
awit_tweets
