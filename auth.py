from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return NotImplemented

@auth.route('/signup')
def signup():
    return NotImplemented
