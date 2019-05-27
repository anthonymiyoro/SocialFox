from django.urls import path
from twitterScraper import views

urlpatterns = [
    path('tweets/', views.tweet_list),
    path('tweets/<int:pk>/', views.tweet_detail),
]