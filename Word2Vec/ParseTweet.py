from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re
import pandas as pd
import externalproperties

# Define a function to split a tweet into parsed sentences
def tweet_to_sentences(tweet, tokenizer, remove_stopwords=False):
    # Function to split a tweet into parsed sentences. Returns a
    # list of sentences, where each sentence is a list of words
    #
    # 1. Use the NLTK tokenizer to split the paragraph into sentences
    raw_sentences = tokenizer.tokenize(tweet.strip())
    #
    # 2. Loop over each sentence
    sentences = []
    for raw_sentence in raw_sentences:
        # If a sentence is empty, skip it
        if len(raw_sentence) > 0:
            # Otherwise, call tweet_to_wordlist to get a list of words
            sentences.append(tweet_to_wordlist(raw_sentence,
                                                remove_stopwords))
    #
    # Return the list of sentences (each sentence is a list of words,
    # so this returns a list of lists
    return sentences


def tweet_to_wordlist(tweet, remove_stopwords=False):
    # tweet_text = BeautifulSoup(tweet).get_text()
    tweet_text = re.sub("[^a-zA-Z]", " ", tweet)
    words = tweet_text.lower().split()
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    return (words)


def clean_parse_tweets(remove_stopwords):
    train = pd.read_csv(externalproperties.TRAIN_DATA_PATH, sep=',',
                        names=['Sentiment', 'Number', 'Date', 'Query', 'Name', 'Text'], dtype=str)
    print train.columns.values
    num_tweets = train["Text"].size
    clean_train_tweets = []

    print "Cleaning and parsing the training set..."
    for i in xrange(0, num_tweets):
        if ((i + 1) % 1000 == 0):
            print "Review %d of %d\n" % (i + 1, num_tweets)
        clean_train_tweets.append(tweet_to_wordlist(train["Text"][i]))

    # Initialize an empty list of sentences
    sentences = []

    print "Parsing sentences from training set..."
    for tweet in train["Text"]:
        sentences.append(tweet_to_wordlist(tweet,
                                            remove_stopwords))
    return sentences
