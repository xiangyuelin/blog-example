# -*- coding: utf-8 -*-

from flask import render_template
from flask import Blueprint
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask import flash
from flask import current_app

from model import Post
from extension import db

web = Blueprint('web', __name__)

@web.route('/posts')
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
        return redirect(url_for('web.list_posts'))


@web.route('/posts/add', methods=['GET', 'POST'])
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


@web.route('/posts/<id>', methods=['GET'])
def show_post(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('show_post.html', post=post)


@web.route('/posts/<id>/delete', methods=['POST'])
def delete_post(id):
    check_authority()
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('web.list_posts'))


@web.route('/posts/<id>/edit', methods=['GET', 'POST'])
def update_post(id):
    if not check_authority():
        flash('Login to access that page!')
        return redirect(url_for('web.signin'))
    post = Post.query.filter_by(id=id).first()

    if request.method == "GET":
        return render_template('put_post.html', post=post)

    # POST
    post.content = request.form.get('content')
    post.title = request.form.get('title')
    post.author = request.form.get('author')
    db.session.commit()
    return redirect(url_for('web.show_post', id=id))



#indentitation
@web.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')

    # POST
    username = request.form.get('username')
    password = request.form.get('password')
    if username != current_app.config['USERNAME'] or password != current_app.config['PASSWORD']:
        flash('username password mismatch!')
        return render_template('signin.html')

    session['logged_in'] = True
    return redirect(url_for('list_posts'))


@web.route('/signout', methods=['GET', 'POST'])
def signout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('.signin'))



def check_authority():
    if not session.get('logged_in'):
        return False
    return True
