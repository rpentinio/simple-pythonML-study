import numpy as np
from sklearn import tree
from sklearn.datasets import load_iris

iris = load_iris()
test_idx = [0, 50, 100]

# training data - remove the 1st, 51st, and 101st rows in the table
# as they should not be part of the data to be used for training the classifier
# (probably to avoid bias)
train_target = np.delete(iris.target, test_idx)
train_data = np.delete(iris.data, test_idx, axis=0)

# testing data - the 1st, 51st, and 101st rows in the table
test_target = iris.target[test_idx]
test_data = iris.data[test_idx]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(train_data, train_target)

print ("expected targets/results: " + str(test_target))
print ("test data: " + str(test_data))
print ("ML prediction: " + str(clf.predict(test_data)))