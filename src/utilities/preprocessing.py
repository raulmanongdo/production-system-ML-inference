import pandas as pd
from sklearn.model_selection import train_test_split as sk_train_test_split
from sklearn.preprocessing import OneHotEncoder

def Xy_split(df, target):
    X = df.copy()
    y = X.pop(target)
    return X, y


def train_test_split(df):
    train, test = sk_train_test_split(df, test_size=0.33)
    return train, test


def preprocess(X):
    # TODO: For the presentation we only care about the solution architecture,
    # not the specifics of the model.
    X = X[['age', 'balance']]
    return X