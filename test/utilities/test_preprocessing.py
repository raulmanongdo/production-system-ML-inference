import pandas as pd
import pytest

from src.utilities import preprocessing
from test.fixtures import df


def test_preprocess(df):
    X = preprocessing.preprocess(df)
    assert set(X.columns) == {'age', 'balance'}
    assert len(X) == len(df)