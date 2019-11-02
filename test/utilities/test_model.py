import pandas as pd
import pytest

from src.utilities.model import Model
from test.fixtures import X, y, model



def test_model_init():
    Model()
    return


def test_model_fit(X, y, model):
    model.fit(X, y)
    return
    

def test_model_predict(X, y, model):
    model.fit(X, y)
    yhat = model.predict(X)
    return