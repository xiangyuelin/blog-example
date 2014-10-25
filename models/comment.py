# -*- coding: utf-8 -*-

from datetime import datetime

from extension import db


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_id_to = db.Column(db.Integer)
    c_content = db.Column(db.Text)

    def get_comment(comment_id):
        comment = Comment.query.get(comment_id)
        return comment

    def add_comment(user_id, user_id_to, content):
        comment = Comment(user_id=user_id, user_id_to=user_id_to, c_content=content)
        db.session.add(comment)
        db.session.commit()

    def delete_comment(comment_id):
        comment = Comment.query.get(comment_id)
        db.session.delete(comment)
        db.session.commit()

