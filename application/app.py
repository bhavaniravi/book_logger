from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import timedelta

import os

load_dotenv()
db_url = os.environ["DATABASE_URL"]

db_url = db_url.replace('postgres', 'postgresql', 1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3000)
db = SQLAlchemy(app)

from application.api import *