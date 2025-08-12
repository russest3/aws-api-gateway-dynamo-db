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

def delete_function(payload):
    try:
        dynamo.delete_item(Key=payload['Key'])
        print(f"Item successfully deleted: {payload['Key']}")
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Item successfully deleted'})
        }
    except:
        logger.error(f"Error deleting item: {payload['Key']}")
        raise

def delete_handler(event, context):
    logger.info(event)
    logger.info('store-data is called')
    print(f"Received event: {json.dumps(event)}")
    delete_function(event['payload'])
