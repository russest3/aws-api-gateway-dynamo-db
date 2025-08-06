import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    book_id = event['pathParameters']['book_id']
    table.delete_item(Key={'book_id': book_id})
    return {'statusCode': 204, 'body': ''}