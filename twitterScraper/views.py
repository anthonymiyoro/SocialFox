from django.http import HttpResponse, JsonResponse
from twitterScraper.models import Tweet
from twitterScraper.serializers import TweetSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# @api_view(['GET'])
# def post_collection(request):
#     if request.method == 'GET':
#         tweets = Tweet.objects.all()
#         serializer = TweetSerializer(tweets, many=True)
#         return Response(serializer.data)


# @api_view(['GET'])
# def post_element(request, pk):
#     try:
#         tweet = Tweet.objects.get(pk=pk)
#     except Tweet.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = TweetSerializer(tweet)
#         return Response(serializer.data)

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

@csrf_exempt
def tweet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
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


