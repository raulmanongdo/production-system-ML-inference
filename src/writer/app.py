import os
try:
    import utilities
except ModuleNotFoundError:
    from . import utilities


TABLE_NAME = os.environ['TABLE_NAME']


def lambda_handler(event, context):
    df = utilities.load_dataframe_from_sqs_event(event)
    utilities.push_to_dynamodb(table_name=TABLE_NAME, dataframe=df)
    return