# -*- coding: utf-8 -*-

from datetime import datetime

from extension import db


class Postlike(db.Model):
    __tablename__ = 'postlikes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

    def get_postlike(pl_id):
        postlike = Postlike.query.get(pl_id)
        return postlike

    def get_all_postlike(user_id):
        postlikes = Postlike.query.filter(user_id=user_id).all()
        return postlikes

    #get user who likes the same post
    def get_all_user_likepost(post_id):
        postlikes = Postlike.query.filter(post_id=post_id)
        return postlikes

    def add_postlike(user_id, post_id):
        postlike = Postlike(user_id=user_id, post_id=post_id)
        db.session.add(postlike)
        db.session.commit()

    def delete_postlike(post_id):
        postlike = Postlike.query.get(post_id)
        db.session.delete(postlike)
        db.session.commit()

