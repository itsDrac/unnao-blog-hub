from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail


app = Flask (__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
admin = Admin(app)
mail = Mail(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config.from_pyfile('config.py')

from blog.routes import *
from blog.admin import *