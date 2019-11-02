"""Builds out the required DynamoDB schema."""
from datetime import datetime
import boto3

METADATA_TABLE_NAME = 'metadata'
CUSTOMER_TABLE_NAME = 'customer' 

db = boto3.client('dynamodb')

metadata_table = db.create_table(
    TableName=METADATA_TABLE_NAME,
    KeySchema=[
        {
            'AttributeName': 'actionID',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'operationDate',
            'KeyType': 'SORT',
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'actionID',
            'KeyType': 'S'
        },
        {
            'AttributeName': 'operationDate',
            'AttributeType': 'S'
        },
    ]
)

customer_table = db.create_table(
    TableName=CUSTOMER_TABLE_NAME,
    KeySchema=[
        {
            'AttributeName': 'customerID',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'creationDate',
            'AttributeType': 'SORT'
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'customerID',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'creationDate',
            'AttributeType': 'S'
        },
    ]
)

timeout = 60 * 10  # Timeout after 10 minutes
start_time = datetime.now()
while (datetime.now() - start_time).total_seconds() < timeout:
    metatable_progress = db.describe_table(TableName=METADATA_TABLE_NAME)
    customer_progress = db.describe_table(TableName=CUSTOMER_TABLE_NAME)
    if (metatable_progress['TableStatus'] == 'ACTIVE' and 
        customer_progress['TableStatus'] == 'ACTIVE'):
        break

duration = (datetime.now() - start_time).total_seconds()
print(f"Tables successfully created! We took {duration} seconds.")