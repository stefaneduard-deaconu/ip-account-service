import random
import string

from app import app
from app import mongo
from flask import render_template_string, request


@app.route('/')
@app.route('/index')
def index():
    db = mongo.db
    users = db.users.find({})
    return render_template_string(
        '''
            <h1> Welcome to the Account Service <h1>
            <div>{{ db }}</div>
            <h2> These are the docs </h2>
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


@app.route('/user', methods=['POST'])
def create_user():
    req_data = request.get_json()
    user = req_data.get('user')
    user_id = generate_user_id(128)
    mongo.db.users.insert_one({**user, "user_id": user_id})
    return '{ "error": false , "user_id":' + user_id + '}'

@app.route('/user', methods=['PUT'])
def update_user():
    req_data = request.get_json()
    user = req_data.get('user')
    mongo.db.docs.update_one(
        {"userName": user.get('userName'), "email": user.get('email')},
        { '$set': user }
    )
    return '{ "error": false}'

@app.route('/user', methods=['DELETE'])
def delete_user():
    req_data = request.get_json()
    mongo.db.docs.delete({"password": req_data.get('password'), "email": req_data.get('email')})
    return '{ "error": false}'

@app.route('/auth', methods=['POST'])
def authenticate_user():
    req_data = request.get_json()
    user = mongo.db.users.find({"email": req_data.get('email'), "password": req_data.get('password')})
    return '{ "error": false , "authToken":' + generate_user_id(32) + '}'



