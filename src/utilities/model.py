import pandas as pd
from sklearn.linear_model import LogisticRegression


class Model():
    """A scikit-learn representation of the ML model.

    This class has been to designed to act as an interface between the scikit-
    learn model and the implementation. Doing so helps us to decouple the 3rd-
    party dependency that exists.

    I've strategically increased the complexity of the system to remove some
    potential technical debt down the line.
    """

    def __init__(self, **hyperparams):
        self.model = LogisticRegression(**hyperparams)

    def fit(self, X, y):
        self.model.fit(X, y)
        return self

    def predict(self, X):
        yhat = pd.Series(self.model.predict(X), index=X.index)
        return yhat
