import pandas as pd


def preprocess(X):
    # TODO: For the presentation we only care about the solution architecture,
    # not the specifics of the model.
    X = X[['age', 'balance']]
    return X