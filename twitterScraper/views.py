from django.http import HttpResponse, JsonResponse
from twitterScraper.models import Tweet
from twitterScraper.serializers import TweetSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status

# Create your views here.

########################## This function returns a JSON object with all the tweets collected so far ###############################
@csrf_exempt
def tweet_list(request):
    """
    List all tweets, or create a new tweet.
    """
    if request.method == 'GET':
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TweetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)





######################## This function analyses the sentiment of a streamers chat collected so far #####################
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def analyse_tweet(request, format=None):
    """
   This function recieves a POST request with a twitter username, after which we search for their
   mentions and return them as a very long JSON string.
    """

    if request.method == 'POST':
        # A serializer allows data to be collected from a POST request
        serializer = TweetSerializer(data=request.data)

        # If the serializer is valid, send twitter username to function that collects and
        # analyses tweets
        if serializer.is_valid():
            try:
                tweet_username = (serializer.validated_data['twitter_user'])
                analysed_json = analyze_data(tweet_username)

            except Exception as e:
                return JsonResponse(str(e), safe=False)
                print(e)

            return JsonResponse(analysed_json, safe=False, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




########################## This function allows for the updating, deleting and putting of tweets. ###############################
@csrf_exempt
def tweet_detail(request, pk):
    """
    Retrieve, update or delete a tweet.
    """
    try:
        tweet = Tweet.objects.get(pk=pk)
    except Tweet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TweetSerializer(tweet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TweetSerializer(tweet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        tweet.delete()
        return HttpResponse(status=204)





