# -*- coding: utf-8 -*-

from datetime import datetime

from extension import db


class Follow(db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_id_following = db.Column(db.Integer)

    def get_follow(follow_id):
        follow = Follow.query.get(follow_id)
        return follow

    def get_all_followings(user_id):
        follows = Follow.query.filter(user_id=user_id).all()
        return follows

    def get_all_followed(user_id_following):
        follows = Follow.query.filter(user_id_following=user_id_following).all()
        return follow

    def add_follow(user_id, user_id_following):
        follow = Follow(user_id=user_id,user_id_following=user_id_followed)
        db.session.add(follow)
        db.session.commit()

    def delete_follow(follow_id):
        follow = Follow.query.get(follow_id)
        db.session.delete(follow)
        db.session.commit()
