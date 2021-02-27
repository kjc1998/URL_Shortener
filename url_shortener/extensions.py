from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
api = Api()
mail = Mail()
admin_USERID = ["NaaJCviCCJ", "qclPmuNLxw"]
