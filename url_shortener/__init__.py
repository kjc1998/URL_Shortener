import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import url_shortener.routes
from .extensions import db, login_manager, bcrypt, api, mail
from .models import User, Link


appF = Flask(__name__)
localHost = False
if os.environ.get('DATABASE_URL') is not None:
    appF.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    appF.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    localHost = True

appF.config['SECRET_KEY'] = '95e1f4ae670667e3338bd65cfe36c773d9b958bb'
appF.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
appF.config['MAIL_SERVER'] = 'smtp.gmail.com'
appF.config['MAIL_PORT'] = 587
appF.config['MAIL_USE_TLS'] = True
appF.config['MAIL_USE_SSL'] = False
appF.config['MAIL_USERNAME'] = os.environ.get('DB_USER')
appF.config['MAIL_PASSWORD'] = os.environ.get('DB_PASS')

appF.register_blueprint(url_shortener.routes.app)

db.init_app(appF)
bcrypt.init_app(appF)
api.init_app(appF)
mail.init_app(appF)

login_manager.init_app(appF)
login_manager.login_view = 'app.login'
login_manager.login_message_category = 'info'

if localHost:
    db.create_all(app=appF)
