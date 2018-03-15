# Dependencies
import datetime as dt
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
                 wait_on_rate_limit=False, wait_on_rate_limit_notify=False)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()


def searchDate():
    pass


def searchToday():
    pass


'''
Below implements user input to conduct twitter extraction and analyses.
'''

# Target user
search_term = input("What do you want to search for on Twitter? ")

# Search until date
search_date = input("Do you want to specify a date? ").lower()

# Potential response lists
yes_list = ["yes", "y", "yep", "yeah", "yea", "sure", "ya", "yah", "ye"]
no_list = ["no", "n", "nah", "nope", "never", "no way", "nein"]

# Conditional to check user input
if search_date in no_list:

    # Run analysis
    print(f"Awesome! Let's do a search for tweets that contain '{search_term}'.")

elif search_date in yes_list:

    while search_date:

        # Specify date
        user_date = input("Try a date. Please use the format, YYYY-MM-DD. ")

        try:
            # Check to see if date format is correct
            object_date = dt.datetime.strptime(user_date, "%Y-%m-%d")

            # Today's date
            today = dt.datetime.now()

            # Days between today's date and entered date
            days_between = (today - object_date).days

            if today < object_date:
                print("Umm...I can't see into the future!\n")
            elif days_between > 7:
                print("You can only search up to 7 days in the past.\n")
            else:
                # Change back to string date
                user_date = dt.datetime.strftime(object_date, "%Y-%m-%d")

                # Add one day to specify true date
                object_date = object_date + dt.timedelta(days=1)

                # Grab date for twitter search api
                until_date = dt.datetime.strftime(object_date, "%Y-%m-%d")

                if user_date:
                    break

        except ValueError:
            print("That's not a valid date. Please check your formatting.\n")
        except:
            raise

    print(f"Awesome! Let's do a search for tweets that contain '{search_term}' "
          f"for the date {user_date}.")

else:

    print("Sorry, there was a problem.")
