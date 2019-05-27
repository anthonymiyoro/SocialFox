from django.db import models

# Create your models here.

# This model stores Tweets collected
class Tweets(models.Model):
    tweet_id = models.CharField()
    tweet = models.CharField()
    date_collected = models.DateTimeField(auto_now_add=True)
    twitter_user = models.CharField("User Name on Twitter")
    number_of_likes = models.IntegerField()
    number_of_retweets = models.IntegerField()
    tweet_device = models.CharField("Device Tweet was collected from", blank=True, null=True)





