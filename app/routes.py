import random
import string

from app import app
from app import mongo
from flask import render_template_string, request, jsonify


@app.route('/')
@app.route('/index')
def index():
    db = mongo.db
    users = db.users.find({})
    return render_template_string(
        '''
            <h1> Welcome to the Account Service <h1>
            <div>{{ db }}</div>
            <h2> These are the Users </h2>
            {% for user in users %}
            <div>{{ user }}</div>
            {% endfor %}
        ''',
        db=db,
        users=users
    )


def generate_user_id(num_char):
    """
    for a user, generate a unique id of nun_char characters
    :return: user_id: str
    """
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(num_char))


@app.route('/user', methods=['GET'])
def read_user():
    req_data = request.get_json()  # it mush be 'password' and 'email'
    user_email = req_data.get('email')
    user_pass = req_data.get('password')
    # we check if it's a new user:
    users = mongo.db.users.find({"email": user_email,
                                "password": user_pass}, {'_id': 0, 'userId': 0})
    if not users.alive:
        return '{ "error": true }'
    user = users.next()
    return jsonify(user=user, error='false')


@app.route('/user', methods=['POST'])
def create_user():
    req_data = request.get_json()
    user = req_data.get('user')
    # we check if it's a new user:
    if mongo.db.users.find({"email": user.get('email')}).count():
        return '{ "error": true }'
    user_id = generate_user_id(128)
    auth_token = generate_user_id(32)
    mongo.db.users.insert_one({**user, "userId": user_id,
                               "authToken": auth_token})
    return '{ "error": false, "authToken": "' + auth_token + '" }'


@app.route('/user', methods=['PUT'])
def update_user():
    req_data = request.get_json()
    user = req_data.get('user')
    # there can be an error, if there's no such user
    query = {"email": user.get('email'), "password": user.get('password')}
    if not mongo.db.users.find(query).count():
        return '{ "error": true}'
    mongo.db.users.update_one(
        query,
        {'$set': user}
    )
    return '{ "error": false}'


@app.route('/user', methods=['DELETE'])
def delete_user():
    req_data = request.get_json()
    query = {"authToken": req_data.get('authToken'),
             "password": req_data.get('password'),
             "email": req_data.get('email')}
    if not mongo.db.users.find(query).count():
        return '{ "error": true }'
    mongo.db.users.delete_one(query)
    return '{ "error": false }'


@app.route('/auth', methods=['GET'])
def authenticate_user():
    req_data = request.get_json()
    query = {"email": req_data.get('email'), "password": req_data.get('password')}
    user_cursor = mongo.db.users.find(query)
    if not user_cursor.alive:
        return '{ "error" : true }'
    user = user_cursor.next()
    return '{ "error": false , "authToken": "' + user.get('authToken') + '" }'





