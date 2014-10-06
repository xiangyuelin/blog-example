# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_sqlalchemy import SQLAlchemy


SECRET_KEY = 'rest api'
DEBUG=True

# databse config
SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/blog-example'

# admin pass
USERNAME='lxy'
PASSWORD='123'


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# setup extentions
db = SQLAlchemy(app)


# Model
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(20))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


# Web contraller
@app.route('/')
def index():
    return redirect(url_for('list_posts'))

@app.route('/posts')
def list_posts():
    posts = Post.query.all()
    return render_template('list_posts.html', posts=posts)


@app.route('/posts/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'GET':
        return render_template('add_post.html')

    # post
    title = request.form.get('title')
    author = request.form.get('author')
    content = request.form.get('content')

    post = Post(title=title, author=author, content=content)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('list_posts'))


# utils
def init_db():
    db.create_all()


if __name__ == '__main__':
    app.run()
