import string
from random import choices
from flask import Flask, request
from flask_restful import Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from .models import User, Link
from .extensions import db, login_manager, bcrypt, api


class Login(Resource):
    def post(self, userName, passWord):
        user = User.query.filter_by(username=userName).first()
        if user and bcrypt.check_password_hash(user.password, passWord):
            return {"userid": user.user_id}
        else:
            abort(404, message="User not recognised")


class Details(Resource):
    def post(self, userID, longURL):
        userLinks = User.query.filter_by(user_id=userID).first()
        urlLinks = userLinks.linkUser
        for link in urlLinks:
            if link.original_url == longURL:
                return {"short_url": link.short_url}

        # Create New
        link = Link(original_url=longURL, user_id=userLinks.id)
        db.session.add(link)
        db.session.commit()

        return {"short_url": link.short_url}


api.add_resource(Login, "/login/<string:userName>/<string:passWord>")
api.add_resource(Details, "/details/<string:userID>/<path:longURL>")
