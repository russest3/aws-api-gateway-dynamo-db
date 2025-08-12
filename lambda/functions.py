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
        print("Item added successfully")
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Item successfully created'})
        }
    except:
        logger.error(f"Error creating item: {payload['Item']}")
        raise

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

def put_function(payload):
    try:
        dynamo.update_item(**{k: payload[k] for k in ['Key', 'UpdateExpression', 
            'ExpressionAttributeNames', 'ExpressionAttributeValues'] if k in payload}
        )
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Item successfully updated'})
        }
    except:
        logger.error(f"Error updating item: {payload['Item']}")
        raise

def delete_function(payload):
    try:
        dynamo.delete_item(Key=payload['Key'])
        logger.info(f"Item deleted: {payload['Key']}")
        print("Item deleted successfully")
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Item successfully deleted'})
        }
    except:
        logger.error(f"Error deleting item: {payload['Key']}")
        raise


def functions_handler(event, context):
    if event['operation'] == 'create':
        post_function(event['payload'])
    
    if event['operation'] == 'read':
        get_function(event['payload'])
    
    if event['operation'] == 'update':
        put_function(event['payload'])
    
    if event['operation'] == 'delete':
        delete_function(event['payload'])