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

def get_function(payload):
    response = dynamo.get_item(Key=payload['Key'])
    print(response)
    return [
            response,
            {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
            }
    ]


def get_handler(event, context):
    logger.info(event)
    logger.info('store-data is called')
    print(f"Received event: {json.dumps(event)}")
    get_function(event['payload'])
