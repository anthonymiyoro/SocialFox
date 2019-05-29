from django.db import models

# Create your models here.

# This model stores Tweets collected
class Tweet(models.Model):
    tweet_id = models.CharField(max_length=500)
    tweet = models.CharField(max_length=500)
    date_collected = models.DateTimeField(auto_now_add=False)
    twitter_user = models.CharField("User Name on Twitter", max_length=50)
    number_of_likes = models.IntegerField()
    number_of_retweets = models.IntegerField()
    tweet_device = models.CharField("Device Tweet was collected from", blank=True, null=True, max_length=50)
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=1, null=True)

    class Meta:
        ordering = ('tweet_id',)





