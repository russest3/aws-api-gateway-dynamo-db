import os
import json
import boto3
import logging
from boto3.dynamodb.conditions import Key

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the DynamoDB client
dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    '''
    Returns all books from the DynamoDB table provided.

    Environment variables:
        - TABLE_NAME: The name of the DynamoDB table scanned.
    '''

    logger.info(f"Received event: {json.dumps(event, indent=2)}")

    # Scan the DynamoDB table to get all books
    books = dynamodb_client.scan(
        TableName=os.environ['TABLE_NAME']
    )

    return {
        "statusCode": 200,
        "body": json.dumps(books['Items'])
    }

# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(os.environ['TABLE_NAME'])

# def handler(event, context):
#     item_id = event.get('pathParameters', {}).get('item_id')
    
#     if item_id:
#         response = table.get_item(Key={'item_id': item_id})
#         return {'statusCode': 200, 'body': json.dumps(response.get('Item', {}))}
#     else:
#         response = table.scan()
#         return {'statusCode': 200, 'body': json.dumps(response.get('Items', []))}