from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

import os

if os.path.isfile('mongo_uri.env'):
    from configparser import ConfigParser
    parser = ConfigParser()
    parser.read('mongo_uri.env')
    mongo = PyMongo(app, uri=parser['Mongo']['MONGO_URI'])
else:
    mongo = PyMongo(app, uri=os.environ["MONGO_URI"])
# import the routes for the flask application
from app import routes

# importing the other packages
from app import ocr

