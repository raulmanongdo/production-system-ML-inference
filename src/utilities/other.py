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


def load_dataframe_from_sqs_event(event_dict):
    dfs = []
    for record in event_dict['records']:
        msg = json.loads(record['body'])
        s3_data_uri = msg['uri']
        dff = pd.read_csv(s3_data_uri)
        dfs.append(dff)
    df = pd.concat(dfs, ignore_index=True)
    return df


def push_results_to_sqs(queue, results):
    body = results.to_json(orient='records', lines=True)
    sqs = boto3.client('sqs')
    return sqs.send_message(
        QueueUrl=queue,
        MessageBody=body,
    )