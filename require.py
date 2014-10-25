# -*- coding: utf-8 -*-

from functools import wraps

from flask import session
from flask import abort
from flask import redirect
from flask import url_for

def require_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'uid' not in session:
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.signin'))
        return f(*args, **kwargs)
    return decorated_function
