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

