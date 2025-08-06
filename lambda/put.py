import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    book_id = event['pathParameters']['book_id']
    updates = json.loads(event['body'])
    
    update_expression = "SET " + ", ".join([f"{k}=:{k}" for k in updates.keys()])
    expression_values = {f":{k}": v for k, v in updates.items()}
    
    table.update_item(
        Key={'book_id': book_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
        ReturnValues="UPDATED_NEW"
    )
    return {'statusCode': 200, 'body': json.dumps(updates)}