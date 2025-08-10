import boto3
import logging
import json

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the DynamoDB table that Lambda will connect to
table_name = "lambda-apigateway-table"

# Create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(table_name)

def get_all_handler(event, context):
    all_items = []
    response = dynamo.scan()
    all_items.extend(response['Items'])
        # Continue scanning if there are more items (pagination)
    while 'LastEvaluatedKey' in response:
        response = dynamo.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        all_items.extend(response['Items'])
    
    for item in all_items:
        print(f"Item retrieved: {item}")

    return all_items