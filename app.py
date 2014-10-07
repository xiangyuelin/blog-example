# -*- coding: utf-8 -*-

from flask import Flask
from flask import url_for
from flask import redirect

from extension import db
from web import web

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
db.init_app(app)

# setup blueprint
app.register_blueprint(web)


@app.route('/')
def index():
    return redirect(url_for('web.list_posts'))


# utils
def init_db():
    db.create_all()


if __name__ == '__main__':
    #db.create_all()
    app.run()
