from flask import Flask, request
from markupsafe import escape
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import firestore

app = Flask(__name__)


# Load the environment variables from the .env file
load_dotenv()

# Application Default credentials are automatically created.
firebase = firebase_admin.initialize_app()
db = firestore.client()

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/add_entry/', methods=['POST'])
def add_entry():
    request_data = request.get_json()

    user = None
    date = None
    content = None

    if request_data:
        if 'user' in request_data:
            user = request.data['user']
        if 'date' in request_data:
            date = request.data['date']
        if 'content' in request_data:
            content = request.data['content']
    
    #adds to database
    directory = db.collection('posts').document(user).document(date)
    directory.set({"content": content})

    return None