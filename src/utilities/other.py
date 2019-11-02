import pandas as pd
import joblib
import boto3
import os
import re
import json
from tempfile import TemporaryDirectory


def split_s3_uri(uri):
    match = re.match(r's3:\/\/(.+?)\/(.+)', uri)
    bucket, key = match.group(1), match.group(2)
    return bucket, key


def load_model(uri):
    bucket, key = split_s3_uri(uri)
    s3 = boto3.client('s3')
    with TemporaryDirectory() as tmpdir:
        tmpfile = os.path.join(tmpdir, 'model.joblib')
        s3.download_file(bucket, key, tmpfile)
        model = joblib.load(tmpfile)
    return model
