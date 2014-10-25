# -*- coding: utf-8 -*-

from extension import db
from .model import User

def get_user_by_name(username):
    user = User.query.filter_by(name=username).first()
    print user
    return user

def get_user(user_id):
    user = User.query.get(user_id)
    return user

def get_all_users():
    users = User.query.all()
    return users

def add_user(username, password, email=None):
    user = User(name=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()

def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

def update_user(user_id, name, password, email):
    user = User.query.get(user_id)
    user.name = name
    user.password = password
    user.email = email
    db.session.commit()
