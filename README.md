## TwitterMentionAnalyser

Python Server that collects and analyses twitter mentions for sentiment.

Consumes a POST request in the form of:

'''

import 
http.client

conn = http.client.HTTPConnection("amiyoro2,pythonanywhere,com")

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"twitter_user\"\r\n\r\n@MigunaMiguna\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    }

conn.request("POST", "analyse_tweet,", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

'''

And returns a JSON response with the structure below, but takes a long time (around 60 seconds :( ).

'''
[
  [
          {
              "TweetLocation": "athi river",
              "NumberofRetweets": 0,
              "NumberofFavourites": 0,
              "DateCreated": "2019-06-06 03:39:53.000000",
              "TweetSentiment": 0,
              "TweetText": "@JoyanneSang @MigunaMiguna @enochcheruiyot1 @KoinangeJeff @xtiandela @stivogichbwoy @monicakiragu_ @citizentvkenya @MikeSonko 407 😀",
              "TweetSource": "Twitter for Android",
              "TweetID": 1136477786598760448
          },
          {
              "TweetLocation": "Thindigua estate kiambu Road",
              "NumberofRetweets": 998,
              "NumberofFavourites": 0,
              "DateCreated": "2019-06-06 03:39:35.000000",
              "TweetSentiment": -1,
              "TweetText": "RT @MigunaMiguna: Mr. @KoinangeJeff: It's unethical to invite a guest for an interview then terminate the interview because of some dubious…",
              "TweetSource": "Twitter for iPhone",
              "TweetID": 1136477712170868736
          },
          {
              "TweetLocation": "Somewhere in la la land.",
              "NumberofRetweets": 998,
              "NumberofFavourites": 0,
              "DateCreated": "2019-06-06 03:39:08.000000",
              "TweetSentiment": -1,
              "TweetText": "RT @MigunaMiguna: Mr. @KoinangeJeff: It's unethical to invite a guest for an interview then terminate the interview because of some dubious…",
              "TweetSource": "Twitter for Android",
              "TweetID": 1136477596164743169
          },
          {
              "TweetLocation": "",
              "NumberofRetweets": 0,
              "NumberofFavourites": 0,
              "DateCreated": "2019-06-06 03:39:04.000000",
              "TweetSentiment": 1,
              "TweetText": "@BBeutah @MigunaMiguna @makodingo @KoinangeJeff @MikeSonko @citizentvkenya He has a passion for the nation",
              "TweetSource": "Twitter for Android",
              "TweetID": 1136477581170155521
          },
          {
              "TweetLocation": "Mombasa, Kenya",
              "NumberofRetweets": 4,
              "NumberofFavourites": 0,
              "DateCreated": "2019-06-06 03:38:40.000000",
              "TweetSentiment": 1,
              "TweetText": "RT @bwanajaha: If u continue supporting Esther Passaris,it shows u like and approve corruption,how can she get air ticket from both nationa…",
              "TweetSource": "Twitter for Android",
              "TweetID": 1136477480817233920
          }
      ]
    ]

'''
