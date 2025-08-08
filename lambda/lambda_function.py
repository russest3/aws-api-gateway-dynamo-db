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

# Define some functions to perform the CRUD operations
def create(payload):
    try:
        dynamo.put_item(Item=payload['Item'])
    except:
        logger.error(f"Error creating item: {payload['Item']}")
        raise

    return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Item created successfully'})
        }

def read(payload):
    try:
        item = dynamo.get_item(Key=payload['Key'])
    except:
        logger.error(f"Error reading item: {payload['Key']}")
        raise

    return [
            item['Item'],
            {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
            }
    ]    

def update(payload):
    try:
        dynamo.update_item(**{k: payload[k] for k in ['Key', 'UpdateExpression', 
        'ExpressionAttributeNames', 'ExpressionAttributeValues'] if k in payload})
    except:
        logger.error(f"Error updating item: {payload['Key']}")
        raise

    return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Item updated successfully'})
        }

def delete(payload):
    try:
        dynamo.delete_item(Key=payload['Key'])
    except:
        logger.error(f"Error deleting item: {payload['Key']}")
        raise

    return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Item deleted successfully'})
        }

def echo(payload):
    return [ 
        payload,
        {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
        }
    ]

operations = {
    'create': create,
    'read': read,
    'update': update,
    'delete': delete,
    'echo': echo,
}

def lambda_handler(event, context):
    logger.info(event)
    logger.info('store-data is called')
    print(f"Received event: {json.dumps(event)}")
    '''Provide an event that contains the following keys:
      - operation: one of the operations in the operations dict below
      - payload: a JSON object containing parameters to pass to the 
        operation being performed
    '''
    
    operation = event['operation']
    payload = event['payload']
    
    if operation in operations:
        return operations[operation](payload)
        
    else:
        raise ValueError(f'Unrecognized operation "{operation}"')