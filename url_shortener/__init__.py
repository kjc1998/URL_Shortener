import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import url_shortener.routes
from .extensions import db, login_manager, bcrypt, api, mail
from .models import User, Link


appF = Flask(__name__)
appF.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"

appF.config['SECRET_KEY'] = "95e1f4ae670667e3338bd65cfe36c773d9b958bb"
appF.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
appF.config['MAIL_SERVER'] = 'smtp.gmail.com'
appF.config['MAIL_PORT'] = 587
appF.config['MAIL_USE_TLS'] = True
appF.config['MAIL_USE_SSL'] = False

appF.config['MAIL_USERNAME'] = "projectester21@gmail.com"
appF.config['MAIL_PASSWORD'] = "mailsender21"
appF.config['MAIL_DEFAULT_SENDER'] = "spArrow@gmail.com"

appF.register_blueprint(url_shortener.routes.app)

db.init_app(appF)
bcrypt.init_app(appF)
api.init_app(appF)
mail.init_app(appF)

login_manager.init_app(appF)
login_manager.login_view = 'app.login'
login_manager.login_message_category = 'info'

with appF.app_context():
    db.create_all()
