from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

import routes
