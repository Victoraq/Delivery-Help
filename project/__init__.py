from flask import Flask
from routes import routes
from auth import auth

app = Flask(__name__)

app.config['delivery-help'] = ' mysql873.umbler.com'
db = SQLAlchemy(app)

app.register_blueprint(routes)
app.register_blueprint(auth)