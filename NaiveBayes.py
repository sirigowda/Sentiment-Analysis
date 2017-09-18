import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
import properties

## Training set contains 500000 positive, negative and neutral tweets each (total 1500000 tweets)
f = pd.read_csv(properties.training_data, sep=',', names=['text', 'sentiment'], dtype=str)
print f.head()


def split_into_lemmas(tweet):
    bigram_vectorizer = CountVectorizer(ngram_range=(1, 3), token_pattern=r'\b\w+\b', min_df=1, encoding='utf-8',
                                        decode_error='ignore')
    analyze = bigram_vectorizer.build_analyzer()
    return analyze(tweet)


bow_transformer = CountVectorizer(encoding='utf-8', decode_error='ignore').fit(f['text'])
print "Fitting done"

text_bow = bow_transformer.transform(f['text'])
tfidf_transformer = TfidfTransformer().fit(text_bow)
# tfidf = tfidf_transformer.transform(text_bow)

text_tfidf = tfidf_transformer.transform(text_bow)

# test file contains the test test of 498 tweets
tweets = pd.read_csv(properties.test_data, sep=',', names=['Text'], dtype=str)
classifier_nb = MultinomialNB(class_prior=None).fit(text_tfidf, f['sentiment'])

sentiments = pd.DataFrame(columns=['text', 'class', 'prob'])
i = 0
# print tweets['Text']
for _, tweet in tweets.iterrows():
    i += 1
    try:
        bow_tweet = bow_transformer.transform(tweet)
        print tweet.values[0]
        # tfidf_tweet = tfidf_transformer.transform(bow_tweet)
        sentiments.loc[i - 1, 'text'] = tweet.values[0]
        sentiments.loc[i - 1, 'class'] = classifier_nb.predict(bow_tweet)[0]
        sentiments.loc[i - 1, 'prob'] = round(classifier_nb.predict_proba(bow_tweet)[0][1], 2) * 10
        prob = round(classifier_nb.predict_proba(bow_tweet)[0][1], 2) * 10

    except Exception as e:
        print e
        sentiments.loc[i - 1, 'text'] = tweet.values[0]

sentiments.to_csv(properties.naivebayes_results, encoding='utf-8')
# print sentiments
