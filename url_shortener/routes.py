import flask
import socket
import string
import urllib
import json
import random
from urllib.parse import quote
import validators
import tldextract
import requests
from sqlalchemy import asc, desc, and_, or_
from flask_mail import Message
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
import url_shortener.REST
from .forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from .models import User, Link
from .extensions import db, bcrypt, api, admin_USERID, mail


app = Blueprint('app', __name__)


def checkPrimaryAdmin():
    if current_user.user_id in admin_USERID:
        current_user.admin = True
        db.session.commit()


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        pass
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('app.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        letters = string.ascii_letters
        userID = ''.join(random.choice(letters) for i in range(10))
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password, user_id=userID)
        db.session.add(user)
        db.session.commit()
        send_verification_email(user)
        flash('Please verify your email before attempting to log in!', 'success')
        return redirect(url_for('app.login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        checkPrimaryAdmin()
        return redirect(url_for('app.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        try:
            if user.verified is not True:
                flash('Login Unsuccessful, please verify your email!', 'danger')
                return redirect(url_for('app.login'))
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('app.home'))
            else:
                flash(
                    'Login Unsuccessful, please check username and password!', 'danger')
        except:
            flash('Login Unsuccessful, please check username and password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('app.home'))


@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    teleDevice = flask.request.headers.get('User-Agent')
    url = 'http://ip-api.com/json/{}'.format(get_client_ip(flask.request))
    userLocation = requests.get(url).json()
    if userLocation['status'] == 'success':
        city = userLocation['city']
        country = userLocation['country']
        # print(city, country)
        if link.location is not None:
            old_dict = json.loads(link.location)
            # print(old_dict)
            try:
                old_dict["city"][city] = int(old_dict["city"][city]) + 1
            except:
                old_dict["city"][city] = 1
            try:
                old_dict["country"][country] = \
                    int(old_dict["country"][country]) + 1
            except:
                old_dict["country"][country] = 1
            print(old_dict)
            link.location = json.dumps(old_dict)
        else:
            new_dict = {"city": {city: 1}, "country": {country: 1}}
            new_dict_json = json.dumps(new_dict)
            link.location = new_dict_json
    else:
        pass
    link.visits = link.visits + 1
    db.session.commit()
    return redirect(link.original_url)


def get_client_ip(flaskRequest):
    if flaskRequest.headers.getlist("X-Forwarded-For"):
        ip = flaskRequest.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = flaskRequest.remote_addr
    return ip


@app.route('/add_link', methods=['POST'])
@login_required
def add_link():
    checkPrimaryAdmin()
    original_url = request.form['original_url']
    if not validators.url(original_url):
        flash('Please insert a valid url', 'danger')
        return redirect(url_for('app.home'))
    checkLink = Link.query.filter(and_(Link.original_url == str(original_url),
                                       Link.user_id == current_user.id)).first()
    if checkLink:
        # Link exists in the database before
        flash('You have created this link before', 'info')
        return redirect(url_for('app.link_page', short=checkLink.short_url))
    ext = tldextract.extract(original_url)
    Domain = ext.domain
    url = "https://textance.herokuapp.com/title/" + quote(original_url)
    response = requests.get(url)
    if response.status_code != 200:
        title = "Unknown Title"
    else:
        title = str(response.content.decode("utf-8"))
    link = Link(original_url=original_url,
                domain_url=Domain, title_url=title, user_id=current_user.id)
    db.session.add(link)
    db.session.commit()
    return redirect(url_for('app.link_page', short=link.short_url))


@app.route('/stats')
@login_required
def stats():
    checkPrimaryAdmin()
    thisUser = User.query.filter_by(user_id=current_user.user_id).first()
    links = Link.query.filter_by(author=current_user).order_by(Link.id).all()
    return render_template('stats.html', links=links)


@app.route('/add_link/<short>', methods=['GET', 'POST'])
def link_page(short):
    link = Link.query.filter_by(short_url=short).first()
    # print(link.location)
    try:
        clickDict = json.loads(link.location)
        cityList = sorted(clickDict["city"].items(),
                          key=lambda item: item[1])[::-1]
        countryList = sorted(
            clickDict["country"].items(), key=lambda item: item[1])[::-1]
        # print(cityList, countryList)
        f5City = cityList[:5]
        f5Country = countryList[:5]
        # print(clickDict)
        cityKeys, cityValues, countryKeys, countryValues = [], [], [], []
        for i in range(min(5, len(f5City))):
            cityKeys.append(f5City[i][0])
            cityValues.append(f5City[i][1])
        for i in range(min(5, len(f5Country))):
            countryKeys.append(f5Country[i][0])
            countryValues.append(f5Country[i][1])
        #print(cityKeys, cityValues, countryKeys, countryValues)
    except:
        cityKeys, cityValues = [], []
        countryKeys, countryValues = [], []

    return render_template('link_added.html',
                           new_link=link.short_url, original_url=link.original_url, link=link,
                           cityKeys=cityKeys, cityValues=cityValues, countryKeys=countryKeys, countryValues=countryValues)


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>404</h1>', 404


@app.route('/admin/<userID>')
@login_required
def admin(userID):
    checkPrimaryAdmin()
    if current_user.admin is not True:
        flash('You have no access to this page', 'danger')
        return redirect(url_for('app.home'))
    users = User.query.order_by(User.id).all()
    return render_template('admin.html', users=users,
                           primaryAdmin=admin_USERID[0], currentUser=current_user)


@app.route('/admin/<userID>', methods=['POST'])
@login_required
def setAdmin(userID):
    checkPrimaryAdmin()
    changedUserID = request.form['submit_button']
    changedUser = User.query.filter_by(user_id=changedUserID).first()
    changedUser.admin = not changedUser.admin
    db.session.commit()
    return redirect(url_for('app.setAdmin', userID=userID))


@app.route("/add_link/delete", methods=['POST'])
@login_required
def delete_link():
    checkPrimaryAdmin()
    link_id = request.form['delete_button']
    link = Link.query.get_or_404(link_id)
    if link.author != current_user:
        abort(403)
    db.session.delete(link)
    db.session.commit()
    flash('Link has been deleted!', 'success')
    return redirect(url_for('app.stats'))


@app.route("/graph")
@login_required
def global_graph():
    checkPrimaryAdmin()

    # global
    links = Link.query.all()
    dictionary = {}
    for link in links:
        try:
            dictionary[link.domain_url] += link.visits
        except:
            dictionary[link.domain_url] = link.visits
    len_dict = len(dictionary)
    sum_dict = sum(dictionary.values())
    dictionary = dict(
        reversed(sorted(dictionary.items(), key=lambda item: item[1])))
    dictionary = dict(list(dictionary.items())[:5])
    dictionary = json.dumps(dictionary)

    # current User
    userLinks = Link.query.filter_by(author=current_user).all()
    currentDictionary = {}
    for link in userLinks:
        try:
            currentDictionary[link.domain_url] += link.visits
        except:
            currentDictionary[link.domain_url] = link.visits
    len_curdict = len(currentDictionary)
    sum_curdict = sum(currentDictionary.values())
    currentDictionary = dict(
        reversed(sorted(currentDictionary.items(), key=lambda item: item[1])))
    currentDictionary = dict(list(currentDictionary.items())[:5])
    currentDictionary = json.dumps(currentDictionary)

    # COUNTRY DATA
    clink = Link.query.filter_by(author=current_user).all()
    cityDict = {}
    countryDict = {}
    # clink will prduce a list [..., ...]
    for link in clink:
        try:
            clickDict = json.loads(link.location)
            cityList = sorted(
                clickDict["city"].items(), key=lambda item: item[1])[-1::]
            countryList = sorted(
                clickDict["country"].items(), key=lambda item: item[1])[-1::]
            f5City = cityList[:5]
            f5Country = countryList[:5]
            cityKeys, cityValues, countryKeys, countryValues, counter = [], [], [], [], []
            for i in range(min(5, len(f5City))):
                cityKeys.append(f5City[i][0])
                cityValues.append(f5City[i][1])
            for key in range(len(cityKeys)):
                if cityKeys[key] in cityDict:
                    cityDict[cityKeys[key]] += (cityValues[key])
                else:
                    cityDict[cityKeys[key]] = cityValues[key]
            for i in range(min(5, len(f5Country))):
                countryKeys.append(f5Country[i][0])
                countryValues.append(f5Country[i][1])
            for key in range(len(countryKeys)):
                if countryKeys[key] in countryDict:
                    countryDict[countryKeys[key]] += (countryValues[key])
                else:
                    countryDict[countryKeys[key]] = countryValues[key]
        except:
            cityKeys, cityValues = [], []
            countryKeys, countryValues = [], []
    cityDict = dict(
        reversed(sorted(cityDict.items(), key=lambda item: item[1])))
    cityDict = dict(list(cityDict.items())[:5])
    cityDict = json.dumps(cityDict)

    countryDict = dict(
        reversed(sorted(countryDict.items(), key=lambda item: item[1])))
    countryDict = dict(list(countryDict.items())[:5])
    countryDict = json.dumps(countryDict)

    # RENDER TEMPLATE
    return render_template('graphBen.html', link=links, linkDict=dictionary,
                           currentLinkDict=currentDictionary, lenDict=len_dict, sumDict=sum_dict,
                           lenCurDict=len_curdict, sumCurDict=sum_curdict, cityLinkDict=cityDict, countryLinkDict=countryDict)


def send_verification_email(user, methods='GET'):
    token = user.get_verification_token()
    user.user_token = token
    db.session.commit()
    msg = Message('Email Verification', recipients=[user.email])
    stringMessage = f"Thank you for registering with us, to complete your registration please visit:\n\
        {url_for('app.verification_token', token=token,  _external=True)}\n\
        If you did not make this request please ignore this email."
    msg.body = stringMessage
    mail.send(msg)


@app.route("/register/<token>")
def verification_token(token):
    user = User.verify_verification_token(token)
    unverified = User.query.filter_by(user_token=token).first()
    if user is None:
        db.session.delete(unverified)
        db.session.commit()
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('app.register'))
    else:
        user.verified = True
        db.session.commit()
        flash('Your email has been verified, you can now login!', 'success')
    return redirect(url_for('app.login'))


def send_reset_email(user, methods='GET'):
    resetoken = user.get_reset_token()
    msg = Message('Password Reset', recipients=[user.email])
    stringMessage = f"To complete your password reset request, please visit the following link:\n\
        {url_for('app.reset_token', resetoken=resetoken,  _external=True)}\n\
        If you did not make this request please ignore this email."
    msg.body = stringMessage
    mail.send(msg)
    return None


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('app.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<resetoken>", methods=['GET', 'POST'])
def reset_token(resetoken):
    if current_user.is_authenticated:
        return redirect(url_for('app.home'))
    user = User.verify_reset_token(resetoken)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('app.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated, you are now able to log in!', 'success')
        return redirect(url_for('app.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
