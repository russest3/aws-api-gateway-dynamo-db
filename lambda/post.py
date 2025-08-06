import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    book = json.loads(event['body'])
    table.put_item(Item=book)
    return {'statusCode': 201, 'body': json.dumps(book)}