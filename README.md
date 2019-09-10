## Twitter Sentiment Harvester (Server)

Python/Django API Server that collects, stores and analyses twitter mentions for sentiment.


And returns a JSON response with the structure below, but takes around 30 seconds :(
```
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
          }
      ]
    ]

```

### Full documentation can be found [here:](https://documenter.getpostman.com/view/1877723/SVmqzLRp?version=latest)
