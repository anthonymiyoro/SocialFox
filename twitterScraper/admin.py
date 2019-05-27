from django.contrib import admin

from .models import Tweets
# Register your models here.

class TweetsAdmin(admin.ModelAdmin):
    fields = ['tweet', 'tweet_id', 'date_collected', 'twitter_user', 'number_of_likes', 'number_of_retweets', 'tweet_device']

admin.site.register(Tweets, TweetsAdmin)