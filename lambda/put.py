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

def put_function(payload):
    dynamo.update_item(**{k: payload[k] for k in ['Key', 'UpdateExpression', 
        'ExpressionAttributeNames', 'ExpressionAttributeValues'] if k in payload}
    )
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Item successfully updated'})
    }


def put_handler(event, context):
    logger.info(event)
    logger.info('store-data is called')
    print(f"Received event: {json.dumps(event)}")
    put_function(event['payload'])