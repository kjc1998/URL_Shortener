import string
from random import choices
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from .extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    verified = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.String(60), nullable=False)
    user_token = db.Column(db.String(2000))
    admin = db.Column(db.Boolean)
    linkUser = db.relationship('Link', backref='author', lazy=True)

    def get_verification_token(self, expires_sec=180):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_verification_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_reset_token(self, expires_sec=180):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(resetoken):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(resetoken)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2000))
    domain_url = db.Column(db.String(2000))
    title_url = db.Column(db.String(2000))
    short_url = db.Column(db.String(5), unique=True)
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()

    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(choices(characters, k=5))

        link = self.query.filter_by(short_url=short_url).first()
        if link:
            return self.generate_short_link()

        def __repr__(self):
            return f"Links('{self.links}')"

        return short_url
