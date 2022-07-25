import boto3

from constants import TODOS_TABLE_NAME
from models.todo import Todo
from uuid import uuid4

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TODOS_TABLE_NAME)


def get_todos():
    response = table.scan()
    todos = [Todo(id=item['id'], message=item['message'])
             for item in response['Items']]
    return todos


def post_todo(message: str):
    id = str(uuid4())
    todo = Todo(id=id, message=message)
    table.put_item(Item={
        'id': todo.id,
        'message': todo.message
    })
    return todo


def put_todo(id: str, message: str):
    todo = Todo(id=id, message=message)
    table.update_item(Key={'id': todo.id},
                      UpdateExpression='SET message = :m',
                      ExpressionAttributeValues={':m': todo.message},
                      TableName=TODOS_TABLE_NAME,
                      )
    return todo


def delete_todo(id: str):
    table.delete_item(
        Key={'id':  id},
        TableName=TODOS_TABLE_NAME,
    )
