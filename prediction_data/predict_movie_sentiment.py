# Dependencies
import json
from pprint import pprint
from datetime import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys

# Grab config file
sys.path.insert(0, '..')
from config import (consumer_key, consumer_secret,
                    access_token, access_token_secret)

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser(),
                 wait_on_rate_limit=False, wait_on_rate_limit_notify=False)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Movie list to predict success
movie_list = ["#Gringo", "#TheHurricaneHeist", "#PreyAtNight", "#WrinkleInTime", "#LoveSimon",
              "#TombRaider", "#PacificRimUprising", "#SherlockGnomes", "#Acrimony",
              "#ReadyPlayerOne"]

# User input to specify search until date
search_date = input(
    "What date do you want to query the movies? Has to be in this format (%Y-%m-%d): ")

# "Real Person" Filters
min_tweets = 5
max_tweets = 10000
max_followers = 2500
max_following = 2500
lang = "en"

# Create list of dictionaries
sentiment = []

# Analyze each movie in list
for movie in movie_list:

    # Assign title as search term
    search_term = movie

    # Create variable for holding the oldest tweet
    oldest_tweet = None

    # List to hold average compound values for each movie
    compound_list = []

    try:

        # Loop through 18 times (total of 1800 tweets)
        for x in range(18):

            # Get all tweets from home feed (for each page specified)
            public_tweets = api.search(search_term,
                                       count=100,
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
                    tweet_text = tweet['text']

                    # Run Vader Analysis on each tweet
                    results = analyzer.polarity_scores(tweet["text"])
                    compound = results["compound"]

                    # Append compound value to list
                    compound_list.append(compound)

                    # Reassign the the oldest tweet (i.e. the max_id)
                    oldest_tweet = int(tweet["id_str"])

                    # Subtract 1 so the previous oldest isn't included
                    # in the new search
                    oldest_tweet -= 1

        # Store average
        tweet_dict = {"Movie Title": search_term,
                      "Search Date": search_date,
                      "Compound": np.mean(compound_list),
                      "Tweet Count": len(compound_list)}

        # Append tweet data to sentiment list
        sentiment.append(tweet_dict)

    except Exception as e:
        print(e)

# Create Dataframe
movie_sent_df = pd.DataFrame(sentiment)

# Reorder columns
movie_sent_df = movie_sent_df.iloc[:, [1, 0, 2, 3]]

# Save to csv
# movie_sent_df.to_csv(f'{search_date}_movie_sentiment.csv',
#                      encoding='utf-8', index=False)
