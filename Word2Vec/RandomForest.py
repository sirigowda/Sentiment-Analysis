# Fit a random forest to the training data, using 100 trees
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import externalproperties

def classify_tweets(X_train, y_train, X_test):
    forest = RandomForestClassifier( n_estimators = 10,max_depth=10 )

    print "Fitting a random forest to labeled training data..."
    forest = forest.fit(X_train,y_train)

    print "Predicting sentiments for test data..."
    result = forest.predict( X_test )

    # Write the test results to output file
    output = pd.DataFrame( data={"text":X_test["Text"][0], "sentiment": result} )
    output.to_csv(externalproperties.RF_OUTPUT_FILE_PATH)