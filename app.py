# -*- coding: utf-8 -*-

from flask import Flask
from flask import url_for
from flask import redirect

from extension import db
from web import web
from admin import admin

SECRET_KEY = 'rest api'
DEBUG=True

# databse config
SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/blog'

# admin pass
AD_NAME = "admin"
AD_PWD = "123"
DEFAULT_UPWD = "123"


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# setup extentions
db.init_app(app)
#

# setup blueprint
#def config_blueprint():
#app.register_blueprint(web)
app.register_blueprint(web, url_prefix='/web')
app.register_blueprint(admin, url_prefix='/admin')
with app.app_context():
    db.create_all()
#def config_db():


# utils
def init_db():
    db.create_all()


if __name__ == '__main__':
    #db.create_all()
    app.run()
