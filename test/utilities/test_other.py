import pandas as pd
import pytest
import os

from src.utilities import other
from test.fixtures import csv_directory


def test_split_s3_uri():
    file_uri = "s3://my-bucket/my/path/to/file.ext"
    dir_uri = "s3://my-bucket/my/directory/"
    assert other.split_s3_uri(file_uri) == ("my-bucket", 'my/path/to/file.ext')
    assert other.split_s3_uri(dir_uri) == ("my-bucket", 'my/directory/')
