from rest_framework import serializers
from twitterScraper.models import Tweet

class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('tweet', 'tweet_id', 'date_collected', 'twitter_user', 'number_of_likes', 'number_of_retweets', 'tweet_device')