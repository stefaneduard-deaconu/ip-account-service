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

# 
# @app.route('/docs', methods=['POST'])
# def upload_docs():
#     req_data = request.get_json()
#     user_id = req_data.get('userId')
#     docs = req_data.get('docs')  # a list of docs
#     for i in range(len(docs)):
#         docs[i]['userId'] = user_id
#     #  lucram cu db
#     db_docs = mongo.db.docs.find({"userId": user_id})
#     db_docs_ids = [doc.get('docId') for doc in db_docs]
#     docs_new = [doc for doc in docs if doc.get('docId') not in db_docs_ids]
#     docs_update = [doc for doc in docs if doc.get('docId') in db_docs_ids]
#     if docs_new:  # this can later be treated as an error, we sent no docs
#         mongo.db.docs.insert_many(docs_new)
#     for doc in docs_update:
#         query = {"docId": doc.get('docId'), 'userId': user_id}
#         updates = {"$set": doc}
#         mongo.db.docs.update_one(query, updates)
#     #
#     return '{ "error": false }'
# 
# 
# @app.route('/docs', methods=['DELETE'])
# def delete_docs():
#     req_data = request.get_json()
#     user_id = req_data.get('userId')
#     #
#     mongo.db.docs.delete_many({"userId": user_id})
#     #
#     return '{ "error": false }'
# 
# 
# @app.route('/docs/<user_id>', methods=['POST'])
# def create_doc(user_id):
#     req_data = request.get_json()
#     doc = req_data.get('doc')
#     doc = {**doc, 'userId': user_id}
#     #
#     mongo.db.docs.insert_one(doc)
#     return '{ "error": false}'
# 
# 
# @app.route('/docs/<user_id>', methods=['PUT'])
# def update_doc(user_id):
#     req_data = request.get_json()
#     doc = req_data.get('doc')
#     doc_id = doc.get('docId')
#     #
#     mongo.db.docs.update_one(
#         {"docId": doc_id, "userId": user_id},
#         { '$set': doc }
#     )
#     #
#     return '{ "error": false}'
# 
# 
# @app.route('/docs/<user_id>', methods=['DELETE'])
# def delete_doc(user_id):
#     req_data = request.get_json()
#     doc_id = req_data.get('docId')
#     #
#     mongo.db.docs.delete_one(
#         {'docId': doc_id, 'userId': user_id}
#     )
#     #
#     return '{ "error": false}'
# 
# 


