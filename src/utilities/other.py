import pandas as pd
import joblib
import boto3
import os
import re
from tempfile import TemporaryDirectory


def split_s3_uri(uri):
    match = re.match(r's3:\/\/(.+?)\/(.+)', uri)
    bucket, key = match.group(1), match.group(2)
    return bucket, key


def download_directory(uri, dst, dst_exist_ok=True):
    """Downloads a directory from S3 onto the local disk."""
    os.makedirs(dst, exist_ok=dst_exist_ok)

    bucket, key = split_s3_uri(uri)
    s3 = boto3.resource('s3')
    bucket_obj = s3.Bucket(bucket)
    for obj in bucket_obj.objects.filter(Prefix=key):
        if obj.key.endswith('/'):
            continue  # Skip over fileless items returned.
        else:
            _, fname = os.path.split(obj.key)
            bucket_obj.download_file(obj.key, os.path.join(dst, fname))
    return 


def read_csv_directory(path):
    """Loads in a CSV directory into a single dataframe."""
    fpaths = [os.path.join(path, f) for f in os.listdir(path)]
    dfs = [pd.read_csv(f, sep=';') for f in fpaths]
    df = pd.concat(dfs, ignore_index=True)
    return df


def save_model(obj, uri):
    """Serialises and uploads the model artifacts into S3."""
    bucket, key = split_s3_uri(uri)
    s3 = boto3.client('s3')
    with TemporaryDirectory() as tmpdir:
        tmpfile = os.path.join(tmpdir, 'model.joblib')
        joblib.dump(obj, tmpfile)
        s3.upload_file(tmpfile, bucket, f"{key}model.joblib")
