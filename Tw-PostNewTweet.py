import tweepy
import os
import pandas as pd
import sys

from twitter.fn_SendEmail import send_error_msg_via_email

# IMPORTANT: In cron tab, run this in the parent directory. E.g. /get-2-twitter-bot

# User Input:
csv_dir = "./sample/output_tweet.csv"

# Fetch environment variable
try:
    consumer_key = os.environ['consumer_key']
    consumer_secret = os.environ['consumer_secret']
    access_token = os.environ['access_token']
    access_token_secret = os.environ['access_token_secret']
    email_password = os.environ['email_password']  # email password

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

    send_error_msg_via_email(error_msg="No environment variables found.", password=email_password)
    sys.exit(1)


# Code to access the account
try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    user = api.me()
    print("This is my user name: "+user.name)
except tweepy.TweepError as e:
    error_code = str(e.args[0][0]['code'])
    error_msg = str(e.args[0][0]['message'])
    print("TweepError: " + error_code + " - " + error_msg)

    send_error_msg_via_email(error_msg=error_msg, password=email_password)
except:
    print("ERROR: Twitter API call failed. Please check your twitter API Access code.")
    send_error_msg_via_email(error_msg="Twitter API call failed.", password=email_password)
    sys.exit(1)

# Select the first line from the output_tweet.csv file
try:
    df_raw = pd.read_csv(csv_dir)

    selected_tweet = df_raw.output_tweet[0]
    print(selected_tweet)
except:
    print(f"ERROR: No csv file found or the file does not contain any tweet! The current dir is: {csv_dir}")
    send_error_msg_via_email(error_msg="No Output CSV files found", password=email_password)
    sys.exit(1)

# post the tweet
try:
    api.update_status(selected_tweet)
    print("New Tweet Posted Successfully!")
except tweepy.TweepError as e:
    error_code = str(e.args[0][0]['code'])
    error_msg = str(e.args[0][0]['message'])
    print("TweepError: " + error_code + " - " + error_msg)

    send_error_msg_via_email(error_msg=error_msg, password=email_password)
    sys.exit(1)

try:
    # exclude the first row 0 from the data frame
    df = df_raw[1:].copy()
    df.to_csv(csv_dir, index=False, header=True)
    print("CSV file updated.")
except:
    print(f"ERROR: Failed to update the csv file. The current dir is: {csv_dir}")
    send_error_msg_via_email(error_msg="Failed to update the csv file", password=email_password)
    sys.exit(1)
