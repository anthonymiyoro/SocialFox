import numpy as np
import pandas as pd
import re
import urllib


from pprint import pprint

import twitter_credentials

import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

########### This function measures the sentiment of a string ###################
analyser = SentimentIntensityAnalyzer()

def sentiment_scorer(tweet):
    # Analyse the sentiment of a comment using VADER sentiment analysis
    score = analyser.polarity_scores(tweet)


    # delete evereything apart from the compuound score']
    for k in list(score.keys()):
        if k != 'compound':
                del score[k]
    return str(score)


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets



# Save tweets to file?????
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, raw_data):
        try:
            print(raw_data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(raw_data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print("Error recieved!!!!", status)


# # # # ANALYSE TWEET LINE BY LINE # # # #
class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    # sanitize tweet
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = sentiment_scorer(self.clean_tweet(tweet))

        # Get and convert sentiment score to decimal
        matches = re.findall("[+-]?\d+\.\d+", analysis)
        analysis = float(matches[0])

        if analysis > 0:
            return 1
        elif analysis == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['name'] = np.array([tweet.user.name for tweet in tweets])
        # pprint ([tweet.user for tweet in tweets])
        df['id'] = np.array([tweet.id for tweet in tweets])
        # df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['location'] = np.array([tweet.user.location for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    """
    Collect tweets from a users timeline
    """
    # # collect tweets from a users timeline
    # tweets = api.user_timeline(screen_name="realDonaldTrump", count=1)

    # df = tweet_analyzer.tweets_to_data_frame(tweets)
    # df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

    """
    Search for topic on twitter and create a dataframe with sentiment, etc
    """
    # Search for mention in tweets
    query = 'okta'
    def query_topic_from_twitter(query):
        max_tweets = 100

        searched_tweets = 0
        last_id = -1

        while searched_tweets < max_tweets:
            count = max_tweets - searched_tweets
            try:
                new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
                if not new_tweets:
                    break
                df = tweet_analyzer.tweets_to_data_frame(new_tweets)
                df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
                searched_tweets = searched_tweets + 1
                last_id = new_tweets[-1].id

            except tweepy.TweepError as e:
                # depending on TweepError.code, one may want to retry or wait
                # to keep things simple, we will give up on an error
                break

        print(df.head(10))


    """
    Get the users who favorited a status using its ID
    """
    def get_user_info_of_post_likes(post_id):
        try:
            json_data = urllib.request.urlopen('https://twitter.com/i/activity/favorited_popup?id=' + str(post_id)).read()
            found_ids = re.findall(r'data-user-id=\\"+\d+', json_data)
            unique_ids = list(set([re.findall(r'\d+', match)[0] for match in found_ids]))
            return unique_ids

        except urllib.request.HTTPError as e:
            pprint (e)
            return False

        # Example:
        # https://twitter.com/golan/status/731770343052972032

        print (get_user_info_of_post_likes(731770343052972032))

        # ['13520332', '416273351', '284966399']
        #
        # 13520332 +> @TopLeftBrick
        # 416273351 => @Berenger_r
        # 284966399 => @FFrink
