import string
import random
from flask import render_template, url_for, flash, redirect, request, Blueprint
from .forms import RegistrationForm, LoginForm
from .models import User, Link
from flask_login import login_user, current_user, logout_user, login_required
import url_shortener.REST
from .extensions import db, bcrypt, api

app = Blueprint('app', __name__)


@app.route("/")
@app.route("/home")
def home():
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
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('app.login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('app.shortener'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('app.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('app.home'))


@app.route("/shortener")
@login_required
def shortener():
    return render_template('shortener.html')


@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    link.visits = link.visits + 1
    db.session.commit()
    return redirect(link.original_url)


@app.route('/add_link', methods=['POST'])
@login_required
def add_link():
    original_url = request.form['original_url']
    link = Link(original_url=original_url)
    db.session.add(link)
    db.session.commit()
    return render_template('link_added.html',
                           new_link=link.short_url, original_url=link.original_url)


@app.route('/stats')
@login_required
def stats():
    links = Link.query.all()
    return render_template('stats.html', links=links)


@app.route('/add_link/<short>', methods=['GET', 'POST'])
def link_page(short):
    original_url = short
    link = Link.query.filter_by(short_url=short).first()
    return render_template('link_added.html',
                           new_link=link.short_url, original_url=link.original_url)


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>404</h1>', 404
