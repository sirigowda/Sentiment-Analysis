import numpy as np
import externalproperties
import pandas as pd
import Word2Vec
from gensim.models import word2vec
# Import the built-in logging module and configure it so that Word2Vec
# creates nice output messages
import logging
import consts
import RandomForest


def makeFeatureVec(words, model, num_features):
    # Function to average all of the word vectors in a given
    # paragraph

    # Pre-initialize an empty numpy array (for speed)
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0.
    # Index2word is a list that contains the names of the words in
    # the model's vocabulary. Convert it to a set, for speed
    index2word_set = set(model.wv.index2word)

    # Loop over each word in the tweet and, if it is in the model's
    # vocaublary, add its feature vector to the total
    for word in words:
        if word in index2word_set:
            nwords = nwords + 1.
            featureVec = np.add(featureVec, model[word])

    # Divide the result by the number of words to get the average
    featureVec = np.divide(featureVec, nwords)
    return featureVec


def getAvgFeatureVecs(tweets, model, num_features):
    # Given a set of tweets (each one a list of words), calculate
    # the average feature vector for each one and return a 2D numpy array
    #
    # Initialize a counter
    counter = 0.

    # Preallocate a 2D numpy array, for speed
    tweetFeatureVecs = np.zeros((len(tweets), num_features), dtype="float32")

    # Loop through the tweets
    for tweet in tweets:
        if counter % 10000. == 0.:
            print "Review %d of %d" % (counter, len(tweets))
        tweetFeatureVecs[counter] = makeFeatureVec(tweet, model,
                                                    num_features)
        counter = counter + 1.
    return tweetFeatureVecs


def train_word2Vec_model(sentences):
    # Initialize and train the model (this will take some time)
    print "Training model..."
    model = word2vec.Word2Vec(sentences, workers=consts.num_workers,
                              size=consts.num_features, min_count=consts.min_word_count,
                              window=consts.context, sample=consts.downsampling)
    # If you don't plan to train the model any further, calling
    # init_sims will make the model much more memory-efficient.
    model.init_sims(replace=True)
    # It can be helpful to create a meaningful model name and
    # save the model for later use. You can load it later using Word2Vec.load()
    model_name = "300features_40minwords_10context"
    model.save(model_name)
    return model


def main():
    clean_train_tweets = []
    clean_test_tweets = []
    remove_stopwords = False

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)

    train = pd.read_csv(externalproperties.TRAIN_DATA_PATH, sep=',',
                        names=['Sentiment', 'Number', 'Date', 'Query', 'Name', 'Text'], dtype=str)
    for tweet in train["Text"]:
        clean_train_tweets.append(Word2Vec.tweet_to_wordlist(tweet, remove_stopwords=True))
    sentences = Word2Vec.clean_parse_tweets(remove_stopwords)
    model = train_word2Vec_model(sentences)
    trainDataVecs = getAvgFeatureVecs(clean_train_tweets, model, consts.num_features)

    test = pd.read_csv(externalproperties.TEST_DATA_PATH, sep=',',
                       names=['Sentiment', 'Number', 'Date', 'Query', 'Name', 'Text'], dtype=str)
    print "Creating average feature vecs for test tweets"
    for tweet in test["Text"]:
        clean_test_tweets.append(Word2Vec.tweet_to_wordlist(tweet, remove_stopwords=True))
    testDataVecs = getAvgFeatureVecs(clean_test_tweets, model, consts.num_features)

    results = RandomForest.classify_tweets(trainDataVecs, train["Sentiment"], testDataVecs)
    results.to_csv(externalproperties.RF_OUTPUT_FILE_PATH)


if __name__ == "__main__":
    main()
