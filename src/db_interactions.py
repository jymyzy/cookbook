from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv


def create_user(db, username: str, password: str):
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(
        sql, {"username": username, "password": generate_password_hash(password)}
    )
    db.session.commit()
    print(f"User {username} created successfully")


def get_user(db, username: str):
    sql = "SELECT * FROM users WHERE username = :username"
    return db.session.execute(sql, {"username": username}).fetchone()


# Returns all ingredients, not for a specific recipe
def get_ingreadients(db):
    sql = "SELECT * FROM ingredients"
    return db.session.execute(sql, {}).fetchall()


def add_recipe(db, name: str, description: str, instructions: str, author_id: int):
    sql = "INSERT INTO recipes (name, desprictions, instructions, author_id, created_on) VALUES (:name, :desprictions, :instructions, :author_id, NOW()) RETURNING id"
    result = db.session.execute(
        sql,
        {
            "name": name,
            "desprictions": description,
            "instructions": instructions,
            "author_id": author_id,
        },
    )
    id = result.fetchone()[0]
    db.session.commit()
    return id


def add_ingredient_to_recipe(
    db, recipe_id: int, ingredient_id: int, amount: int, unit: str
):
    sql = "INSERT INTO ingredientsInRecipe (recipe_id, ingredient_id, amount, unit) VALUES (:recipe_id, :ingredient_id, :amount, :unit)"
    db.session.execute(
        sql,
        {
            "recipe_id": recipe_id,
            "ingredient_id": ingredient_id,
            "amount": amount,
            "unit": unit,
        },
    )
    db.session.commit()
