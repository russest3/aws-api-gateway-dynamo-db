import os
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    item_id = event.get('pathParameters', {}).get('item_id')
    
    if item_id:
        response = table.get_item(Key={'item_id': item_id})
        return {'statusCode': 200, 'body': json.dumps(response.get('Item', {}))}
    else:
        response = table.scan()
        return {'statusCode': 200, 'body': json.dumps(response.get('Items', []))}