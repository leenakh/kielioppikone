import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db


def register(username, password, role, first_name, last_name):
    if 4 < len(username) < 20 and 7 < len(password) < 20:
        hash_value = generate_password_hash(password)
        try:
            sql = "INSERT INTO users (username, password, role, first_name, last_name) \
                VALUES (:username, :password, :role, :first_name, :last_name)"
            db.session.execute(
                sql, {"username":username, "password":hash_value, "role":role, "first_name":first_name, "last_name":last_name})
            db.session.commit()
        except:
            return False
        return login(username, password)


def login(username, password):
    sql = "SELECT id, username, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role
        session["csrf_token"] = secrets.token_hex(16)
        return True
    return False


def user_id():
    return session.get("user_id", 0)

def username():
    return session.get("username", 0)


def is_user():
    return session.get("role") == "user"


def is_admin():
    return session.get("role") == "admin"

def is_teacher():
    return session.get("role") == "teacher"

def logout():
    del session["user_id"]
    del session["username"]
    del session["role"]
    return True
