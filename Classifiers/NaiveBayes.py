import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
import externalproperties

# Splits tweet into lemmas
def split_into_lemmas(tweet):
    bigram_vectorizer = CountVectorizer(ngram_range=(1, 3), token_pattern=r'\b\w+\b', min_df=1, encoding='utf-8',
                                        decode_error='ignore')
    analyze = bigram_vectorizer.build_analyzer()
    return analyze(tweet)

# Trains the classifier and predicts sentiment for test data set
def naive_bayes_classify(f, tweets):

    # Fit data using bag of words(bow) transformer
    bow_transformer = CountVectorizer(encoding='utf-8', decode_error='ignore').fit(f['text'])
    text_bow = bow_transformer.transform(f['text'])

    # Fit using tf-idf transformer
    tfidf_transformer = TfidfTransformer().fit(text_bow)
    text_tfidf = tfidf_transformer.transform(text_bow)

    # Train the multinomial naive bayes classifier
    classifier_nb = MultinomialNB(class_prior=None).fit(text_tfidf, f['sentiment'])

    # classify tweets in test data (tweets)
    sentiments = pd.DataFrame(columns=['text', 'class', 'prob'])
    i = 0
    for _, tweet in tweets.iterrows():
        i += 1
        try:
            bow_tweet = bow_transformer.transform(tweet)
            print tweet.values[0]
            sentiments.loc[i - 1, 'text'] = tweet.values[0]
            sentiments.loc[i - 1, 'class'] = classifier_nb.predict(bow_tweet)[0]
            sentiments.loc[i - 1, 'prob'] = round(classifier_nb.predict_proba(bow_tweet)[0][1], 2) * 10
            prob = round(classifier_nb.predict_proba(bow_tweet)[0][1], 2) * 10
        except Exception as e:
            print e
            sentiments.loc[i - 1, 'text'] = tweet.values[0]
    print sentiments
    return sentiments

def main():
    # Training set contains 500000 positive, negative and neutral tweets each (total 1500000 tweets)
    f = pd.read_csv(externalproperties.training_data, sep=',', names=['text', 'sentiment'], dtype=str)
    print f.head()

    # Test file contains the test set of 498 tweets
    tweets = pd.read_csv(externalproperties.test_data, sep=',', names=['Text'], dtype=str)

    # Train the classifier and classify data
    sentiments = naive_bayes_classify(f, tweets)

    # Write the results to np_test_results file
    sentiments.to_csv(externalproperties.np_test_results, encoding='utf-8')

if __name__ == "__main__":
    main()
