﻿from flask import Flask
import url_shortener.routes
from .extensions import db, login_manager, bcrypt, api
from flask_sqlalchemy import SQLAlchemy


appF = Flask(__name__)
appF.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
appF.config['SECRET_KEY'] = '95e1f4ae670667e3338bd65cfe36c773d9b958bb'
appF.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
appF.register_blueprint(url_shortener.routes.app)

db.init_app(appF)
bcrypt.init_app(appF)
api.init_app(appF)

login_manager.init_app(appF)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# create database, won't overwrite existing storage
db.create_all(app=appF)
