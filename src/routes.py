from flask import Flask, request, render_template, redirect, session
from werkzeug.security import check_password_hash
from app import app, db

from db_interactions import create_user, get_user


# Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = get_user(db, username)
        if user == None:
            return render_template(
                "error.html", error="Käyttäjää ei löytynyt", return_to="/"
            )
        if check_password_hash(user.password, password):
            session["username"] = username
            session["user_id"] = user.id
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
    del session["user_id"]
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
