from flask import Blueprint, redirect, url_for, request, session
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
import json

from project import db
from models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    user = User.getUserByEmail(data['email'])
    
    if not user or not check_password_hash(user.password, data['password']):
        return json.dumps({'message': 'Wrong credentials'})

    login_user(user)

    access_token = create_access_token(identity=data['email'])
    refresh_token = create_refresh_token(identity=data['email'])

    login_data = {
        'email': data['email'],
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    return json.dumps(login_data)

@auth.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()

    user = User.getUserByEmail(email=data['email'])

    if user: # if user already exists return a error message
        return json.dumps({'message': 'User already exists'})

    new_user = User(
        name=data['name'], email=data['email'], password=generate_password_hash(data['password']),
        longitude=data['longitude'], latitude=data['latitude'], 
        telephone=data['telephone'], role=data['role']
        )

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=data['email'])
    refresh_token = create_refresh_token(identity=data['email'])

    signup_data = {
        'email': data['email'],
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    return json.dumps(signup_data)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return json.dumps({'success': '200'}), 200, {'ContentType':'application/json'}