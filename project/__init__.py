from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ

app = Flask(__name__)

try:
    app.config.from_pyfile('app.cfg')
except:
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['MAX_CONTENT_LENGTH'] = environ.get('MAX_CONTENT_LENGTH')
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
    app.config['SESSION_TYPE'] = environ.get('SESSION_TYPE')
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

# Configure the database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
jwt = JWTManager(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes blueprints
from routes import routes
from auth import auth
app.register_blueprint(routes)
app.register_blueprint(auth)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()