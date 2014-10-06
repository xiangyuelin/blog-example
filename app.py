# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask import flash
from flask import abort
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


@app.route('/posts', methods=['GET', 'POST'])
def list_posts():
    posts = Post.query.all()
    if request.method == 'GET':
        return render_template('list_posts.html', posts=posts)
    else:
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        post = Post(title=title, author=author, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('list_posts'))


@app.route('/posts/add', methods=['GET', 'POST'])
def add_post():
    check_authority()
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


@app.route('/posts/<id>', methods=['GET', 'PUT', 'DELETE'])
def show_post(id):
    post = Post.query.filter_by(id=id).first()
    if request.method == "GET":
        return render_template('show_post.html', post=post)
    elif request.method == 'PUT':
        post.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('show_post', id=id))
    else:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('list_posts'))


@app.route('/posts/<id>/delete', methods=['POST'])
def delete_post(id):
    check_authority()
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('list_posts'))


@app.route('/posts/<id>/put', methods=['GET', 'POST'])
def put_post(id):
    check_authority()
    post = Post.query.filter_by(id=id).first()
    if request.method == "POST":
        post.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('show_post', id=id))
    return render_template('put_post.html', post=post)



#indentitation
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
    return render_template('signin.html', error=error)


@app.route('/signout', methods=['GET', 'POST'])
def signout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('signin'))


def check_authority():
    if not session.get('logged_in'):
        abort(401)


# utils
def init_db():
    db.create_all()


if __name__ == '__main__':
    #db.create_all()
    app.run()
