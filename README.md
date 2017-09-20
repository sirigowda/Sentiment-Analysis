# Sentiment-Analysis

### ABOUT THE CODE
Extract tweets from Twitter's Streaming API based on any keywords.

### SYSTEM REQUIREMENTS

Operating System : Windows / Mac OS X

Programming Language: Python 2.7

### FILE DESCRIPTIONS

##### EXTRACT TWEETS FOLDER

Extract tweets folder contains the StreamTweets.py file using which we can extract tweets from Twitter's Streaming API. StreamTweets.py uses **tweepy**, a Python library to access Twitter, which must be downloaded. The pip command to install it is `pip install tweepy` 

Tweets are extracted based on specified keywords, which can be added in the properties.py file in the same folder. A user account must be created on Twitter as well, so as to obtain access_token, access_token_secret, consumer_key and consumer_secret which must be set in the properties file. 

Running StreamTweets.py will extract tweets containing the keywords specified.

