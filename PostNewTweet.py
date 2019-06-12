import tweepy
import os
import pandas as pd
import sys

# User Input:
csv_dir = "./sample/test_output_tweet1.csv"

# Fetch environment variable
try:
    consumer_key = os.environ['consumer_key']
    consumer_secret = os.environ['consumer_secret']
    access_token = os.environ['access_token']
    access_token_secret = os.environ['access_token_secret']

    print(f'Current working directory: {os.getcwd()}')
    print("=" * 30)
    print("Twitter API Credential:")
    print(consumer_key[:5])
    print(consumer_secret[:5])
    print(access_token[:5])
    print(access_token_secret[:5])
    print("=" * 30)
except:
  print("ERROR: No environment variables found.")
  print("Please add consumer_key, consumer_secret,access_token and access_token_secret.")
  sys.exit(1)


# Code to access the account
try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    user = api.me()
    print("This is my user name: "+user.name)
except:
    print("ERROR: Twitter API call failed. Please check your twitter API Access code.")
    sys.exit(1)

# Select the first line from the output_tweet.csv file
try:
    df_raw = pd.read_csv(csv_dir)

    selected_tweet = df_raw.output_tweet[0]
    print(selected_tweet)
except:
    print(f"ERROR: No csv file found or the file does not contain any tweet! The current dir is: {csv_dir}")
    sys.exit(1)

# post the tweet
try:
    api.update_status(selected_tweet)
    print("New Tweet Posted Successfully!")
except:
    print("ERROR: Failed to post tweet.")
    sys.exit(1)

try:
    # exclude the first row 0 from the data frame
    df = df_raw[1:].copy()
    df.to_csv(csv_dir, index=False, header=True)
    print("CSV file updated.")
except:
    print(f"ERROR: Failed to update the csv file. The current dir is: {csv_dir}")
    sys.exit(1)
