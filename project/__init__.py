from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config.from_pyfile('app.cfg')

# Configure the database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
jwt = JWTManager(app)

# Routes blueprints
from routes import routes
from auth import auth
app.register_blueprint(routes)
app.register_blueprint(auth)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()