import boto3
import json
import pandas as pd

def load_dataframe_from_sqs_event(event_dict):
    dfs = []
    for record in event_dict['records']:
        msg = SQSMessage()
        msg.read_event_record(record)
        dfs.append(msg.dataframe)
    df = pd.concat(dfs, ignore_index=True)
    return df


class SQSMessage:

    def __init__(self):
        self._dataframe = None
        return

    def read_event_record(self, event):
        self._dataframe = event['body'].read_json(orient='records', lines=True)
        return self

    @property 
    def dataframe(self):
        return self._dataframe

    @dataframe.setter 
    def dataframe(self, df):
        self._dataframe = df

    def send(self, queue):
        if not isinstance(self._dataframe, pd.DataFrame):
            raise RuntimeError(
                "You need to either assign a dataframe to the message or load "
                "in an event dictionary."
            )

        metadata = {}  # TODO
        data = self._dataframe.to_json(orient='records', lines=True)
        body = {'metadata': metadata, 'data': data}

        sqs = boto3.client('sqs')
        return sqs.send_message(QueueUrl=queue, MessageBody=body)
