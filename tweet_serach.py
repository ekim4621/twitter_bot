#!/usr/bin/env python3
import pandas as pd
import os
import tweepy as tw
import twitter_cred as tc
import getpass
import json

output_file = '/Users/{user}/Downloads/retrieved_tweets.csv'.format(user=getpass.getuser())

def set_session():
    # Authenticate to Twitter
    auth = tw.OAuthHandler(tc.consumer_key, tc.consumer_secret)
    auth.set_access_token(tc.access_token, tc.access_token_secret)
    
    # Create API object
    api = tw.API(auth)

    # Verify authentication
    try:
        api.verify_credentials()
        print('Authentication OK')
    except:
        print('Error authenticating, check credentials. Exiting program.')
        exit()
    return api


def get_tweets():
    """
    Version 1: 
        - This call will do a GLOBAL search to retreive results that have 'cat' or 'dog' anywhere within the tweet, description, hashtag, username, etc.
          Given this, someone with cat or dog within their username e.g. denverCatlover, could be tweeting about bitcoin and would still qualify to be in
          the search results.

    Version 2 iteration feature notes: 
        - Return results that explicitly contain cats or dogs within the text of the tweet, hashtag, or contain an image of a cat or dog. 
        - Method to qualify a tweet that only contains an image of a cat or dog without any text indicator. 
    """
    search_results = api.search(q='cats OR dogs -#caturday filter:media -filter:retweets -filter:replies'   # Search query
                                , lang='en'                                                                 # Language of tweet
                                , result_type='recent'                                                      # Retrieve by most recent 
                                , tweet_mode='extended'                                                     # Retrieve expanded tweet                                                   
                                , count=100)                                                                # Number of tweets to retrieve 
    print('Retreiving most recent tweets about cats or dogs...')

    # Explore tweet properties
    # print(dir(search_results[0]))
    # exit()    
    
    # Explore user details
    # print(json.dumps(search_results[0].user._json, indent=4))
    # exit()

    # Open a pandas dataframe, insert full tweet text
    tweet_df = pd.DataFrame(data=[tweet.full_text for tweet in search_results], columns=['Full_tweet'])

    # Populate additional fields 
    tweet_df['Create_date'] = [tweet.created_at for tweet in search_results]
    tweet_df['Display_name'] = [tweet.user._json['name'] for tweet in search_results]
    tweet_df['User_name'] = [tweet.user._json['screen_name'] for tweet in search_results]
    tweet_df['Tweet_id'] = [tweet.id for tweet in search_results]
    tweet_df['Favorite_count'] = [tweet.favorite_count for tweet in search_results]
    tweet_df['Retweet_count'] = [tweet.retweet_count for tweet in search_results]

    # Rearrange fields
    tweet_df = tweet_df[['Create_date', 'Display_name', 'User_name', 'Tweet_id', 'Favorite_count', 'Retweet_count', 'Full_tweet']]

    # Export to csv
    print('Output file located: {output_file}'.format(output_file=output_file)) 
    return tweet_df.to_csv(output_file, header=True, index=False, sep=',', escapechar='\\', encoding='utf-8-sig')


if __name__ == '__main__':
    api = set_session()
    get_tweets()
    







