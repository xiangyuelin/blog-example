# -*- coding: utf-8 -*-

from datetime import datetime

from extension import db
from .model import Post

def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return post

def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()

def add_post(title, content, user_id):
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

def update_post(content, post_id):
    post = Post.query.filter_by(id=post_id).first()
    #post.title = title
    #post.author = author
    post.content = content
    post.updated_at = datetime.now()
    db.session.commit()

def get_posts_by_user(user_id):
    posts = Post.query.filter_by(user_id=user_id).all()
    return posts


def get_all_posts():
    posts =  Post.query.all()
    return posts

def get_posts_by_user(user_id):
    posts = Post.query.filter_by(user_id=user_id).all()
    return posts
