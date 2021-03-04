import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import url_shortener.routes
from .extensions import db, login_manager, bcrypt, api, mail
from .models import User, Link


appF = Flask(__name__)
appF.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

appF.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
appF.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
appF.config['MAIL_SERVER'] = 'smtp.gmail.com'
appF.config['MAIL_PORT'] = 587
appF.config['MAIL_USE_TLS'] = True
appF.config['MAIL_USE_SSL'] = False

appF.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
appF.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

appF.register_blueprint(url_shortener.routes.app)

db.init_app(appF)
bcrypt.init_app(appF)
api.init_app(appF)
mail.init_app(appF)

login_manager.init_app(appF)
login_manager.login_view = 'app.login'
login_manager.login_message_category = 'info'
