from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)

try:
    app.config.from_pyfile('app.cfg')
except:
    app.config.from_envvar('SQLALCHEMY_DATABASE_URI')
    app.config.from_envvar('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config.from_envvar('MAX_CONTENT_LENGTH')
    app.config.from_envvar('JWT_SECRET_KEY')
    app.config.from_envvar('SESSION_TYPE')
    app.config.from_envvar('SECRET_KEY')

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