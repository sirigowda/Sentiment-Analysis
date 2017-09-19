# Sentiment Analysis using OneVsRestClassifier
import properties
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn import preprocessing

# Trains the classifier with X_train and predicts value for X_test
def onevsrest_classify(X_train, y_train, X_test):
    lb = preprocessing.LabelBinarizer()
    Y = lb.fit_transform(y_train)

    # Multiclass classifier
    classifier = Pipeline([
        ('vectorizer', CountVectorizer(encoding='utf-8', decode_error='ignore')),
        ('tfidf', TfidfTransformer()),
        ('clf', OneVsRestClassifier(LinearSVC()))])

    classifier.fit(X_train, Y)
    predicted = classifier.predict(X_test)
    all_labels = lb.inverse_transform(predicted)

    sent = pd.DataFrame(columns=['text', 'class'])
    i = 1
    for item, labels in zip(X_test, all_labels):
        sent.loc[i, 'text'] = item
        sent.loc[i, 'class'] = ''.join(labels)
        i += 1
    return sent

def main():
    # Training set contains 500000 positive, negative and neutral tweets each (total 1500000 tweets)
    f = pd.read_csv(properties.training_data, sep=',', names=['Sentiment', 'Number', 'Date', 'Query', 'Name', 'Text'],
                    dtype=str)
    X_train = f['Text']
    y_train = f['Sentiment']

    # Test file contains the test set of 498 tweets
    tweets = pd.read_csv(properties.test_data, sep=',', names=['Text'], dtype=str)
    X_test = tweets['Text']

    # Train the classifier and classify data
    sentiments = onevsrest_classify(X_train, y_train, X_test)

    # Write the results to onevsrest_results file
    sentiments.to_csv(properties.onevsrest_results, encoding='utf-8')

if __name__ == "__main__":
    main()