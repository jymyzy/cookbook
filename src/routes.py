from collections import namedtuple
from flask import Flask, request, render_template, redirect, session
from werkzeug.security import check_password_hash
from app import app, db

from db_interactions import (
    create_user,
    get_user,
    get_ingreadients,
    add_recipe,
    add_ingredient_to_recipe,
)


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


@app.route("/createRecipe", methods=["GET", "POST"])
def create_recipe():
    ingredients = get_ingreadients(db)

    Ingredient = namedtuple("Ingredient", ["id", "name"])
    Selected_ingredient = namedtuple("Ingredient", ["id", "amount", "unit"])

    # Make sure all ingredients are capitalized
    ingredients = [
        Ingredient(ingredient[0], ingredient[1].capitalize())
        for ingredient in ingredients
    ]

    selected_ingredients = []

    if request.method == "POST":
        name = request.form["recipeName"]
        description = request.form["recipeDescription"]
        instructions = request.form["recipeInstructions"]

        # Create a list of selected ingredients
        for key in request.form.keys():
            if "ingredientQuantity" in key:
                id = int(key.replace("ingredientQuantity", ""))
                ingredient = Selected_ingredient(
                    id,
                    request.form[f"ingredientQuantity{id}"],
                    request.form[f"ingredientUnit{id}"],
                )
                selected_ingredients.append(ingredient)

        recipe_id = add_recipe(db, name, description, instructions, session["user_id"])

        for ingredient in selected_ingredients:
            add_ingredient_to_recipe(
                db, recipe_id, ingredient.id, ingredient.amount, ingredient.unit
            )
        return redirect("/")
    else:
        return render_template(
            "create_recipe.html",
            ingredients=ingredients,
            selected_ingredients=selected_ingredients,
        )
