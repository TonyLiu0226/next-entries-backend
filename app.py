from flask import Flask, request
from flask_cors import CORS
from markupsafe import escape
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import firestore
from flask import Response
from uuid import uuid4
import datetime

app = Flask(__name__)

CORS(app)
# Load the environment variables from the .env file
load_dotenv()

# Application Default credentials are automatically created.
firebase = firebase_admin.initialize_app()
db = firestore.client()

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/add_entry/', methods=['POST'])
# Request parameters:
# user: The unique user ID for the user who made the post
# date: The date of the post, format must be (YYYY-MM-DD)
# content: The post's content
def add_entry():
    request_data = request.get_json()

    user = None
    date = None
    content = None

    if request_data:
        if 'user' in request_data:
            user = request_data['user']
        if 'date' in request_data:
            date = request_data['date']
        if 'content' in request_data:
            content = request_data['content']
    
    try:
        if user == None or date == None or content == None:
            return Response(f"Upload failed, invalid fields", status=400)
        #adds to database
        directory = db.collection("Users").document(user).collection("posts").document(str(uuid4()))
        #splits date
        formattedDate = datetime.datetime(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]), 12, 00, 00)
    
        directory.set({"date": formattedDate, "content": content})
    except Exception as e:
        print(e)
        return Response(f"Upload failed due to exception: {e}", status=500)
    
    return Response("Upload successful", status=200)