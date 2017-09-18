# Find the Accuracy, Specificity, Sensitivity and Confusion matrix of the results
import pandas as pd
import properties
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

# Append the actual results in the test set and corresponding tweets with the predicted results to calculate accuracy
measures = pd.read_csv(properties.naivebayes_results, sep=',',
                       names=['SlNo', 'Text', 'Calc_sentiment', 'Prob', 'Act_sentiment', 'Text_r'], dtype=str)

y_pred = measures['Calc_sentiment']
y_true = measures['Act_sentiment']

accuracy_rate = accuracy_score(y_true, y_pred) * 100
error_rate = (1 - accuracy_score(y_true, y_pred)) * 100

print "accuracy_rate:", accuracy_rate
print "error_rate:", error_rate

conf_matx = confusion_matrix(y_true, y_pred)
print "confusion_matrix:"
print conf_matx

sensitivity = float(conf_matx[0, 0]) / float((conf_matx[0, 0] + conf_matx[0, 1]))
print('Sensitivity : ', sensitivity)

specificity = float((conf_matx[1, 1]) / float(conf_matx[1, 0] + conf_matx[1, 1]))
print('Specificity : ', specificity)
