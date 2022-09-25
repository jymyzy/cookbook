from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
from dotenv import load_dotenv

load_dotenv()

from db_interactions import create_user, get_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

# Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = get_password_hash(db, username)
        if check_password_hash(password, password_hash):
            session["username"] = username
            return redirect("/")
        else:
            return ""
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        create_user(db, username, password)
        return redirect("/")

    return render_template("register.html")
