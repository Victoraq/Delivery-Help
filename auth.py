from flask import Blueprint, redirect, url_for, request, session
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return {'message': 'Wrong credentials'}

    login_user(user)

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)

    return {
        'email': email,
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@auth.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()

    email = data['email']
    password = data['password']
    username = data['username']

    user = User.query.filter_by(email=email).first()

    if user: # if user already exists return a error message
        return {'message': 'User already exists'}

    new_user = User(email=email, username=username, password=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=data['username'])
    refresh_token = create_refresh_token(identity=data['username'])
    return {
        'email': email,
        'access_token': access_token,
        'refresh_token': refresh_token
    }

