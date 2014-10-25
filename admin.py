# -*- coding: utf-8 -*-

from flask import render_template
from flask import Blueprint
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask import flash
from flask import current_app

from models import post_service
from models import user_service
from extension import db
from require import require_admin

admin = Blueprint('admin', __name__)

@admin.route('/')
@admin.route('/posts')
@require_admin
def list_all_posts():
    #posts = Post.query.all()
    posts = post_service.get_all_posts()
    users={}
    for post in posts:
        users[post.id] = user_service.get_user(post.user_id)
    #print posts
    return render_template('admin_list_posts.html', posts=posts, users=users)


@admin.route('/users')
@require_admin
def list_users():
    users = user_service.get_all_users()
    return render_template('list_users.html', users=users)


@admin.route('/users/add', methods=['GET', 'POST'])
@require_admin
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')

    #post
    uname = request.form.get('username')
    upwd = current_app.config['DEFAULT_UPWD']
    user_service.add_user(uname, upwd)
    return redirect(url_for('.list_users'))



@admin.route('/users/<user_id>/delete', methods=['POST'])
@require_admin
def delete_user(user_id):
    user_service.delete_user(user_id)
    return redirect(url_for('.list_users'))


@admin.route('/<user_id>/posts')
@require_admin
def list_posts(user_id):
    posts = post_service.get_posts_by_user(user_id)
    users = {}
    for post in posts:
        users[post.id] = user_service.get_user(post.user_id)
    return render_template('admin_list_posts.html', posts=posts, users=users)


"""
@admin.route('/posts/add', methods=['GET', 'POST'])
@require_admin
def add_post():
    user_id = session['uid']
    if request.method == 'GET':
        return render_template('admin_add_post.html')

    #post
    title = request.form.get('title')
    author = request.form.get('author')
    content = request.form.get('content')
    post_service.add_post(title=title, author=author, content=content, user_id=user_id)
    posts = post_service.get_posts_by_user(user_id)
    return render_template('admin_list_posts.html', posts=posts)
"""

@admin.route('/posts/post/delete', methods=['POST'])
@require_admin
def delete_post():
    post_id = request.form.get('post_id')
    print type(post_id)
    post = post_service.get_post(post_id)
    user_id = post.user_id
    post_service.delete_post(post_id)
    return redirect(url_for('admin.list_posts', user_id=user_id))


@admin.route('/posts/<post_id>', methods=['GET'])
@require_admin
def show_post(post_id):
    if request.method == 'GET':
        post = post_service.get_post(post_id)
        return render_template('admin_show_post.html', post=post)


#indentitation
@admin.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('admin_signin.html')

    # POST
    adminname = request.form.get('adname')
    password = request.form.get('password')
    print adminname, password
    #user = User.query.filter_by(name=username).first()
    if adminname != current_app.config['AD_NAME'] or password != current_app.config['AD_PWD']:
        flash('username password mismatch!')
        return render_template('admin_signin.html')
    #logged_in
    #session['logged_in'] = True
    session['admin'] = 'admin'
    return redirect(url_for('admin.list_all_posts'))


@admin.route('/signout', methods=['GET', 'POST'])
def signout():
  #session.pop('logged_in', None)
  session.pop('admin', None)
  flash('You were logged out')
  return redirect(url_for('.signin'))
