import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db


def register(username_entered, password, role, first_name, last_name):
    hash_value = generate_password_hash(password)
    try:
        sql = "insert into users (username, password, role, first_name, last_name) \
            values (:username_entered, :password, :role, :first_name, :last_name)"
        db.session.execute(sql, {
            "username_entered":username_entered, 
            "password":hash_value, 
            "role":role, 
            "first_name":first_name, 
            "last_name":last_name})
        db.session.commit()
    except:
        return False
    return login(username_entered, password)


def login(username_entered, password):
    sql = "select id, username, password, role from users \
        where username=:username_entered"
    result = db.session.execute(sql, {
        "username_entered":username_entered})
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


def exists(username_entered):
    sql = "select 1 from users \
        where username = :username_entered"
    result = db.session.execute(sql, {
        "username_entered":username_entered})
    if result.fetchone():
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
    del session["csrf_token"]
    return True


def logged_in():
    return user_id() != 0


def owner_of(users_id):
    return user_id() == users_id
