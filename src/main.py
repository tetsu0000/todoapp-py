import awsgi
from flask import (
    Flask,
    jsonify,
    request
)
from controllers.controller import(delete_todo, get_todos, post_todo, put_todo)

app = Flask(__name__)


@app.route('/todos', methods=['GET'])
def get_todos_router():
    response = get_todos()
    return jsonify({
        'message': 'Get todos succeed.',
        'data': response
    })


@app.route('/todos', methods=['POST'])
def post_todo_router():
    response = post_todo(request.json['message'])
    return jsonify({
        'message': 'Post todo succeed.',
        'data': response
    })


@app.route('/todos/<id>', methods=['PUT'])
def put_todo_router(id):
    response = put_todo(id=id, message=request.json['message'])
    return jsonify({
        'message': 'Put todo succeed.',
        'data': response
    })


@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo_router(id):
    delete_todo(id=id)
    return jsonify({
        'message': 'Delete todo succeed.',
    })


def handler(event, context):
    return awsgi.response(app, event, context)
