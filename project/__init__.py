from flask import Flask
from routes import routes
from auth import auth

app = Flask(__name__)

app.register_blueprint(routes)
app.register_blueprint(auth)