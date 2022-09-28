from flask import Flask, request, render_template, redirect, session
from werkzeug.security import check_password_hash
from app import app, db

from db_interactions import create_user, get_password_hash


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
        if check_password_hash(password_hash, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template(
                "error.html", error="Väärä salasana tai käyttäjänimi", return_to="/"
            )

    if request.method == "GET":
        return render_template("login.html")


@app.route("/logout", methods={"POST"})
def logout():
    del session["username"]
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        create_user(db, username, password)
        return redirect("/")

    if request.method == "GET":
        return render_template("register.html")
