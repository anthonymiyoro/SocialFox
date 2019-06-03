from rest_framework import serializers
from twitterScraper.models import Tweet

#Directly add Tweet to DB
class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('tweet', 'tweet_id', 'date_collected', 'twitter_user', 'number_of_likes', 'number_of_retweets', 'tweet_device')

# Collect a users tweets
class TwitterAnalyserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = ('twitter_user',)

    def to_internal_value(self, data):
        twitter_user = data.get('twitter_user')

        # Perform data validation
        if not twitter_user:
            raise serializers.ValidationError({
                'twitter_user': 'This field is required.'
            })

        return {
            'twitter_user': twitter_user
        }
