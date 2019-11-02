import boto3
import numpy as np
import pandas as pd

def push_to_dynamodb(table_name, dataframe, batch_size=100):
    for _, df in dataframe.groupby(np.arange(len(dataframe)) // batch_size):
        put_dataframe(table_name=table_name, df=df)
    return


def put_dataframe(table_name, df):
    """PUTs a dataframe into DynamoDB."""
    dynamodb = boto3.client('dynamodb')
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for _, row in df.iterrows():
            batch.put_item(
                Item=row.to_dict()
            )