import pandas as pd
import pytest
from tempfile import TemporaryDirectory
import os

from src.utilities.model import Model
from src.utilities.preprocessing import Xy_split, preprocess

def load_df():
    data = pd.read_csv('test/data/bank.csv', sep=';')
    return data 


@pytest.fixture
def df():
    return load_df()


@pytest.fixture
def model():
    """Initialises a model with all of the default hyperparameters."""
    return Model()
