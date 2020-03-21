from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from routes import routes
from auth import auth

app = Flask(__name__)

app.config.from_pyfile('app.cfg')

# Configure the database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Routes blueprints
app.register_blueprint(routes)
app.register_blueprint(auth)

login_manager = LoginManager()
login_manager.init_app(app)