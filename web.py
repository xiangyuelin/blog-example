# -*- coding: utf-8 -*-

from flask import render_template
from flask import Blueprint
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask import flash
from flask import current_app

from service import Post
from service import User
from extension import db
from require import require_user

web = Blueprint('web', __name__)


@web.route('/')
@web.route('/posts')
def list_all_posts():
    posts = Post.get_all_posts()
    users={}
    for post in posts:
        users[post.id] = User.get_user(post.user_id)
    #print posts
    return render_template('list_posts.html', posts=posts, users=users)

"""
@web.route('/users')
def list_users():
    users = user_service.get_all_users()
    return render_template('list_users.html', users=users)
"""

@web.route('/<user_id>/posts')
def list_posts(user_id):
    posts = Post.get_posts_by_user(user_id)
    users = {}
    for post in posts:
        users[post.id] = User.get_user(post.user_id)
    return render_template('list_posts.html', posts=posts, users=users)


@web.route('/users/<user_id>/updateinfo', methods=['GET', 'POST'])
@require_user
def update_user(user_id):
    if request.method == 'GET':
        user = User.get_user(user_id)
        return render_template('update_user.html', user=user)
    #post
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    User.update_user(user_id, username, password, email)
    flash('update user information successfully')
    session.pop('uid', None)
    return redirect(url_for('.signin'))


@web.route('/posts/add', methods=['GET', 'POST'])
@require_user
def add_post():
    user_id = session['uid']
    if request.method == 'GET':
        return render_template('add_post.html')

    #post
    title = request.form.get('title')
    #author = request.form.get('author')
    content = request.form.get('content')
    Post.add_post(title=title, content=content, user_id=user_id)
    #posts = post_service.get_posts_by_user(user_id)
    return redirect(url_for('.list_posts', user_id=user_id))
    #render_template('list_posts.html', posts=posts)


@web.route('/posts/post/delete', methods=['POST'])
@require_user
def delete_post():
    post_id = request.form.get('post_id')
    #print type(post_id)
    post = Post.get_post(post_id)
    user_id = post.user_id
    #post = post_service.get_post(post_id)
    #if session['uid'] != user_id
       # flash('Unauthorized! You are not the author!')
        #return redirect(url_for('web.list_all_posts'))
    #authorized
    Post.delete_post(post_id)
    return redirect(url_for('web.list_posts', user_id=user_id))


@web.route('/posts/<post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    if request.method == 'GET':
        post = Post.get_post(post_id)
        user_id = post.user_id
        user = User.get_user(user_id)
        return render_template('show_post.html', post=post, user=user)

    #post
    #title = request.form.get('title')
    #author = request.form.get('author')
    content = request.form.get('content')
    Post.update_post(content=content, post_id=post_id)
    return redirect(url_for('web.show_post', post_id=post_id))


@web.route('/posts/post/update', methods=['POST'])
@require_user
def update_post():
    post_id = request.form.get('post_id')
    print post_id
    post = Post.get_post(post_id)
    return render_template('update_post.html', post=post)


#indentitation
@web.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')

    # POST
    username = request.form.get('username')
    password = request.form.get('password')
    print username, password
    #user = User.query.filter_by(name=username).first()
    user = User.get_user_by_name(username)
    print user
    if user is None:
        flash('user does not exist!')
        return render_template('signin.html')
    elif password != user.password:
        flash('username password mismatch!')
    #logged_in
    #session['logged_in'] = True
    session['uid'] = user.id
    return redirect(url_for('web.list_posts', user_id=session['uid']))

@web.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    # POST
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    print username, password, email
    #user = User.query.filter_by(name=username).first()
    User.add_user(username, password, email)

    return render_template('signin.html')


@web.route('/signout', methods=['GET', 'POST'])
@require_user
def signout():
    session.pop('uid', None)
    flash('You were logged out')
    return redirect(url_for('.signin'))


