import random
import tweepy
import os
import sys

# twitter API credential
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


# related functions
# delete friends once reach the threshold
def remove_frd_from_existing_list(api=tweepy.API(auth), max_frd_num=4500, del_frd_num=100):
    try:
        frd_list = api.friends_ids(id=api.me().id)
        frd_list = set(frd_list)
        print(f"{len(frd_list)} friends found.")

        if len(frd_list) >= max_frd_num:
            print(f"The frd list is too long, {del_frd_num} frds to be removed")

            # randomly remove N users from the list:
            del_frd_list = random.sample(frd_list, del_frd_num)
            for del_user_id in del_frd_list:
                print(f'remove frd: {del_user_id}')
                api.destroy_friendship(user_id=del_user_id)
        else:
            print("The current frd list is below the number threadhold.")

    except:
        print("ERROR: Check remove_frd_from_existing_list")

    return


def list_new_users_from_search_words(search_words="#AI", include_retweet=True):
    if include_retweet:
        new_search = search_words
    else:
        new_search = search_words + " -filter:retweets"

    tweets = tweepy.Cursor(api.search,
                           q=new_search,
                           lang="en").items(100)

    user_list = [[tweet.user.id] for tweet in tweets]
    user_list = [user for user_sub in user_list for user in user_sub]
    user_list = set(user_list)

    print(f"{len(user_list)} users found based on the search word")

    return user_list


def list_existing_frd(api=tweepy.API(auth)):
    frd_list = api.friends_ids(id=api.me().id)
    frd_list = set(frd_list)
    print(f"{len(frd_list)} friends found.")

    return frd_list


def add_new_frds(new_user_list):
    # Add the new users to your friend list
    new_frd_list = []

    for user_id in new_user_list:
        try:
            print(user_id)
            api.create_friendship(user_id=user_id)
            new_frd_list.append(user_id)
        except:
            print("ERROR: Max new friends exceed.")
            break

    print(f"{len(new_frd_list)} new friends have been added.")

    return new_frd_list


def fav_new_frd_tweets(new_frd_list, api=tweepy.API(auth)):
    try:
        for new_frd_id in new_frd_list:

            # find the two most recent tweets from new friend
            tweets = api.user_timeline(user_id=new_frd_id, count=2)

            # like these two tweets
            for tweet in tweets:
                try:
                    api.create_favorite(tweet.id)
                    print("tweet liked.")
                except tweepy.TweepError as e:
                    print(e.reason)
                    print("ERROR: Unable to like new friends' tweets - Inner loop")
                    break
                except:
                    print("ERROR: Unable to like new friends' tweets - Inner loop")

    except tweepy.TweepError as e:
        print(e.reason)
        print("ERROR: Unable to like new friends tweets - Outer loop")
    except:
        print("ERROR: Unable to like new friends tweets - Outer loop")

    return


# process
# pick a search word from the list
search_words_list = ["#NLP",
                    "#python",
                    "#ML",
                    "#MachineLearning",
                    "#AI",
                    "#ArtificialIntelligence",
                    "#future",
                    "#Robot",
                    "#Technology",
                    "#Innovation",
                    "#tech",
                    "#datascience",
                    "#DeepLearning",
                    "#DL",
                    "#Marketing",
                    "GPU", "smart", "machine", "future", "technology",
                    "data", "science", "marketing", "fun", "innovation",
                    "like", "fun", "crazy", "believe", "human", "great"]

search_words = random.choice(search_words_list)

# check to make sure the friend list is < 4000 by default.
remove_frd_from_existing_list()

# find user tweeted with search words
user_list = list_new_users_from_search_words(search_words)

# fetch the existing frd list
frd_list = list_existing_frd()

# List users who are not in the current friend list
new_user_list = (user_list - frd_list)
print(f"{len(new_user_list)} users are not on your existing friend list")

# Add the new users to your friend list
new_frd_list = add_new_frds(new_user_list)

# favourite new friends' tweets
fav_new_frd_tweets(new_frd_list)

# End of the script
print("Successfully add new friends")
