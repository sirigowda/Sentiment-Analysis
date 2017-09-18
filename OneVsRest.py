## Sentiment Analysis using OneVsRestClassifier
import properties
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn import preprocessing

f = pd.read_csv(properties.training_data, sep=',', names=['Sentiment', 'Number', 'Date', 'Query', 'Name', 'Text'],
                dtype=str)
X_train = f['Text']
y_train_text = f['Sentiment']

tweets = pd.read_csv(properties.test_data, sep=',', names=['Text'], dtype=str)
X_test = tweets['Text']
target_names = ['0', '4']

lb = preprocessing.LabelBinarizer()
Y = lb.fit_transform(y_train_text)

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
sent.to_csv(properties.onevsrest_results, encoding='utf-8')
