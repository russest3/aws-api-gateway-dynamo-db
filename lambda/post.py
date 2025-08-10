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

def post_function(payload):
    try:
        dynamo.put_item(Item=payload['Item'])
        logger.info(f"Item added: {payload['Item']}")
        print(f"Item added successfully")
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Item successfully created'})
        }
    except:
        logger.error(f"Error creating item: {payload['Item']}")
        raise

def post_handler(event, context):
    logger.info(event)
    logger.info('store-data is called')
    print(f"Received event: {json.dumps(event)}")
    post_function(event['payload'])
