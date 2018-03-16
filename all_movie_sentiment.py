# Dependencies
from datetime import datetime as dt
import pandas as pd
import numpy as np
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import (consumer_key, consumer_secret,
                    access_token, access_token_secret)

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser(),
                 wait_on_rate_limit=False, wait_on_rate_limit_notify=False)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Movie csv path
csv_path = 'box_office_data/moviesFinal.csv'

# Read csv
movie_df = pd.read_csv(csv_path)

# # "Real Person" Filters
# min_tweets = 5
# max_tweets = 10000
# max_followers = 2500
# max_following = 2500
# lang = "en"

# Create list of dictionaries
sentiment = []

for title in movie_df['title']:

    # Assign title as search term
    search_term = title

    # Create variable for holding the oldest tweet
    oldest_tweet = None

    # List to hold average compound values for each movie
    compound_list = []

    try:

        # Get all tweets from home feed (for each page specified)
        public_tweets = api.search(search_term,
                                   count=100,
                                   lang='en',
                                   result_type="recent",
                                   max_id=oldest_tweet)

        # Loop through all tweets
        for tweet in public_tweets['statuses']:

            # Use filters to check if user meets conditions
            # if (tweet["user"]["followers_count"] < max_followers and
                # tweet["user"]["statuses_count"] > min_tweets and
                # tweet["user"]["statuses_count"] < max_tweets and
                # tweet["user"]["friends_count"] < max_following and
                # tweet["user"]["lang"] == lang):

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
        tweet_dict = {"title": search_term,
                      "compound": np.mean(compound_list),
                      "tweet_count": len(compound_list)}

        # Append tweet data to sentiment list
        sentiment.append(tweet_dict)

    except Exception as e:
        print(e)

# Create dataframe
movie_sent_df = pd.DataFrame(sentiment)

# Reorder columns
movie_sent_df = movie_sent_df[["title", "compound", "tweet_count"]]

# Today's date
today = dt.strftime(dt.now(), "%Y-%m-%d")

# Save to csv
# movie_sent_df.to_csv(f'all_movie_data/{today}_all_movie_sent.csv', encoding='utf-8', index=False)

# Merge dataframes
merged_df = pd.merge(movie_df, movie_sent_df, how="left")

# Save to csv
# merged_df.to_csv(f'all_movie_data/{today}_all_movie_data.csv', encoding='utf-8', index=False)
