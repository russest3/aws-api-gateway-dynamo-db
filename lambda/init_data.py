import os
import boto3
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    print("table is " + table)

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
    try:
      for book in sample_books:
        table.put_item(Item=book)
        return {
          "status": "SUCCESS",
          "message": "Sample books added to database"
        }
    except:
       print("Error inserting sample books")
       return {
          "status": "ERROR",
          "message": "Error inserting sample books"
        }
