import pandas as pd
from sklearn.metrics import roc_auc_score 


def label_encode(y):
    """Converts the string values for y into integers (for easy evaluation)."""
    mapper = {'yes': 1, 'no': 0}
    return y.map(mapper)


def evaluate(y_actual, y_predict):
    y_actual, y_predict = label_encode(y_actual), label_encode(y_predict)
    auc = roc_auc_score(y_actual, y_predict)
    return {'auc': auc}