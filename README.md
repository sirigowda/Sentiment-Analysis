# Sentiment-Analysis

### ABOUT THE CODE

#### EXTRACT TWEETS 

Extract tweets folder contains the StreamTweets.py file using which we can extract tweets from Twitter's Streaming API. StreamTweets.py uses **tweepy**, a Python library to access Twitter, which must be downloaded. The pip command to install it is `pip install tweepy` 

Tweets are extracted based on specified keywords, which can be added in the properties.py file in the same folder. A user account must be created on Twitter as well, so as to obtain access_token, access_token_secret, consumer_key and consumer_secret which must be set in the properties file. 

Running **StreamTweets.py** will extract tweets containing the keywords specified.

#### CLASSIFIERS

The Naive Bayes and the OneVsRest classifiers can be found in this folder. Python libraries **pandas** and **sklearn** need to be installed to run these programs. 

The input and output file paths need to be set in the external properties folder. The training data and test data used is the **Sentiment140 data set** available online.

**NaiveBayes.py**, trains a Multinomial Naive Bayes classifier using the training data, and predicts the sentiment for the test data.
**OneVsRest.py**, trains a Linear Support Vector Machine classifier using the training data, and predicts the sentiment for the test data. OneVsRest is used to clasify tweets into positive, negative and neutral, i.e. for multiclass classification. For only binary classification, Naive Bayes is more efficient.

To determine the accuracy, error rate, confusion matrix, sensitivity and specificity, run **Accuracy.py** on the results.

#### WORD2VEC 

The Word2Vec neural network draws relationships between words upon training and is used with the Random Forest algorithm to classify tweets.

Python libraries **pandas**, **word2vec** and **sklearn** need to be installed to run these programs.

**Word2Vec.py** calls **ParseTweets.py** to convert tweets to word lists and parses them. It then trains the Word2Vec model and obtains the average feature vecor for each of the tweets. **RandomForest.py** is called internally, it trains the model using these vectors and classifies tweets. 

The accuracy, error rate and other metrics can be determined by running the **Accuracy.py** program.




