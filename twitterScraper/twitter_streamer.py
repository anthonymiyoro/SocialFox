import json, re, datetime

import twitterScraper.twitter_credentials

import tweepy
from tweepy import API, Cursor, OAuthHandler, Stream
from tweepy.streaming import StreamListener

from pprint import pprint

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# from models.py import Tweet

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
        auth = OAuthHandler(twitterScraper.twitter_credentials.CONSUMER_KEY, twitterScraper.twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitterScraper.twitter_credentials.ACCESS_TOKEN, twitterScraper.twitter_credentials.ACCESS_TOKEN_SECRET)
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

    def tweets_to_dictionary(self, tweets):

        tweet_analyzer = TweetAnalyzer()

        # Create a list that will store dicitonary of tweets
        tweet_list = []

        # loop through tweets collected
        for tweet in tweets:

            # pprint ("####################  Tweet starts here  #######################")
            # pprint (tweet.text)
            # pprint (tweet.id)
            # pprint (tweet.created_at)
            # pprint (tweet.user.location)
            # pprint (tweet.source)
            # pprint (tweet.favorite_count)
            # pprint (tweet.retweet_count)

            # Calculate sentiment of tweet using vadersentiment
            sentiment = tweet_analyzer.analyze_sentiment(tweet.text)

            # Convert datetime tweet to string
            tweet_datetime_obj = datetime.datetime.strftime(tweet.created_at, '%Y-%m-%d %H:%M:%S.%f')

            # Append different parts of tweet to dictionary
            tweet_dictionary = {"TweetText": tweet.text, "TweetID": tweet.id, "DateCreated": tweet_datetime_obj, "TweetLocation": tweet.user.location,
            "TweetSource": tweet.source, "NumberofFavourites": tweet.favorite_count, "NumberofRetweets": tweet.retweet_count, "TweetSentiment":sentiment}

            # Append the multiple dictionaries to list
            tweet_list.append(tweet_dictionary)

        # pprint (tweet_list)
        return tweet_list



    """
    Search for topic on twitter and create a JSON object with sentiment, etc
    """
    # Search for mention in tweets numbering the same as max_tweets
    # query = '@WilliamsRuto'
    def query_topic_from_twitter(self, query):
        # Instanciate classes
        twitter_client = TwitterClient()
        api = twitter_client.get_twitter_client_api()

        tweet_analyzer = TweetAnalyzer()

        max_tweets = 50
        searched_tweets = 0
        last_id = -1
        list_of_tweets = []

        #Search for the number of tweets specified in max_tweets
        while searched_tweets < max_tweets:
            count = max_tweets - searched_tweets
            try:
                new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
                if not new_tweets:
                    break

                # Collected tweets returns a dictionary of 1 tweet
                collected_tweets = tweet_analyzer.tweets_to_dictionary(new_tweets)
                list_of_tweets.append(collected_tweets)

                searched_tweets = searched_tweets + 1
                last_id = new_tweets[-1].id
                    # pprint (json_result)

                    # # Write chat message and channel name to database
                    # ChatLogs.objects.create(
                    #     message=resp,
                    #     streamer_name=channel_name,
                    #     # created_on=formatedDate
                    # )

                  # Convert python dictionary to JSON
                # json_result = json.dumps(list_of_tweets, ensure_ascii=False).decode(list_of_tweets)
                json_result = json.loads(json.dumps(list_of_tweets, ensure_ascii=False))
                pprint ("JSON RESULT")


            except tweepy.TweepError as e:
                # depending on Tweepy Error.code, one may want to retry or wait
                # to keep things simple, we will give up on an error
                pprint (e)
                break




        return (json_result)



if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    # tweet_analyzer.query_topic_from_twitter("@WilliamsRuto")

