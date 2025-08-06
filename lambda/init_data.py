import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    # Sample book data
    sample_books = [
        {
            "book_id": "B001",
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "year": 1925,
            "genre": "Classic"
        },
        {
            "book_id": "B002",
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "year": 1960,
            "genre": "Fiction"
        },
        {
            "book_id": "B003",
            "title": "1984",
            "author": "George Orwell",
            "year": 1949,
            "genre": "Dystopian"
        }
    ]

    # Insert sample books
    for book in sample_books:
        table.put_item(Item=book)

    return {
        "status": "SUCCESS",
        "message": "Sample books added to database"
    }