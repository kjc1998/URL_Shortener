import string
import json
from random import choices
from urllib.parse import quote
import validators
import requests
import tldextract
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
        if not validators.url(longURL):
            abort(404, message="Please pass in a valid link")
            return None

        # check previous links
        urlLinks = userLinks.linkUser
        for link in urlLinks:
            if link.original_url == longURL:

                # return dictionary
                linkDICT = vars(link)
                del linkDICT['_sa_instance_state']
                linkDICT['date_created'] = linkDICT['date_created'].strftime(
                    "%m/%d/%Y, %H:%M:%S")
                linkJSON = json.dumps(linkDICT)
                return linkJSON

        # create new links
        ext = tldextract.extract(longURL)
        domain = ext.domain
        url = "https://textance.herokuapp.com/title/" + quote(longURL)
        response = requests.get(url)
        if response.status_code != 200:
            title = "Unknown Title"
        else:
            title = str(response.content.decode("utf-8"))
        link = Link(original_url=longURL, domain_url=domain,
                    title_url=title, user_id=userLinks.id)
        db.session.add(link)
        db.session.commit()

        # return dictionary of the newly created link
        newLink = Link.query.filter_by(id=link.id).first()
        linkDICT = vars(newLink)
        del linkDICT['_sa_instance_state']
        linkDICT['date_created'] = linkDICT['date_created'].strftime(
            "%m/%d/%Y, %H:%M:%S")
        linkJSON = json.dumps(linkDICT)
        return linkJSON


api.add_resource(Login, "/login/<string:userName>/<string:passWord>")
api.add_resource(Details, "/details/<string:userID>/<path:longURL>")
