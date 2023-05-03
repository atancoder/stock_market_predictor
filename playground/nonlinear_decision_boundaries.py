# mypy: ignore-errors
import random
from functools import partial
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


"""
Logistic Regression does a fairly decent job at classifying the data. But once I tailor the test data
to be more specific to the X, Y boundaries, the model does not do as well. 
The linear model doesn't really fit the right decision boundary for the data.
"""

X_BOUNDARY = 3
Y_BOUNDARY = 2


def generate_train_data() -> Any:
    data = []
    labels = []
    for _ in range(1000):
        x = random.randint(0, 50)
        y = random.randint(0, 10)
        data.append((x, y))
        if x > X_BOUNDARY and y < Y_BOUNDARY:
            labels.append(1)
        else:
            labels.append(0)
    return data, labels


def generate_test_data() -> Any:
    # test data is more specific to tailor around X, Y boundaries
    data = []
    labels = []
    for _ in range(100):
        x = X_BOUNDARY + random.uniform(-2, 2)
        y = Y_BOUNDARY + random.uniform(-2, 2)
        data.append((x, y))
        if x > 3 and y < 2:
            labels.append(1)
        else:
            labels.append(0)
    return data, labels


def elevate_data(data):
    # use Gaussian kernel to elevate data
    

def plot_decision_boundary(training_data, training_labels, predict_fn):
    # Plot the data points
    X = np.array(training_data)
    y = np.array(training_labels)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap="viridis")
    x1_min, x1_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    x2_min, x2_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx1, xx2 = np.meshgrid(
        np.linspace(x1_min, x1_max, 100), np.linspace(x2_min, x2_max, 100)
    )
    Z = predict_fn(np.c_[xx1.ravel(), xx2.ravel()])
    Z = Z.reshape(xx1.shape)
    plt.contour(xx1, xx2, Z, colors="k", levels=[0])

    plt.show()


def linear_model():
    training_data, training_labels = generate_train_data()
    test_data, test_labels = generate_test_data()

    # linear model
    clf = LogisticRegression()
    clf.fit(training_data, training_labels)
    weights = clf.coef_[0]
    intercept = clf.intercept_[0]
    print("Weights: ", weights)
    print("Intercept: ", intercept)

    accuracy = clf.score(test_data, test_labels)
    print("Accuracy: ", accuracy)
    plot_decision_boundary(training_data, training_labels, clf.predict)


def nonlinear_model():
    training_data, training_labels = generate_train_data()
    test_data, test_labels = generate_test_data()

    def new_predict(clf, data):
        new_data = elevate_data(data)
        return clf.predict(new_data)

    # nonlinear model
    new_training_data = elevate_data(training_data)
    new_test_data = elevate_data(test_data)
    clf = LogisticRegression()
    clf.fit(new_training_data, training_labels)
    weights = clf.coef_[0]
    intercept = clf.intercept_[0]
    print("Weights: ", weights)
    print("Intercept: ", intercept)

    accuracy = clf.score(new_test_data, test_labels)
    print("Accuracy: ", accuracy)

    plot_decision_boundary(training_data, training_labels, partial(new_predict, clf))


nonlinear_model()
