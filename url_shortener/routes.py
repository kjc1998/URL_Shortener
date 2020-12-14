from flask import Blueprint

short = Blueprint('short', __name__)


@short.route('/<short_url>')
def redirect_to_url(short_url):
    pass


@short.route('/')
def index():
    pass


@short.route('/add_link', methods=['POST'])
def add_link():
    pass


@short.route('/stats')
def stats():
    pass


@short.errorhandler(404)
def page_not_found(e):
    return '', 404