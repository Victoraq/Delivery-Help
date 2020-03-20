from flask import Blueprint

routes = Blueprint('routes', __name__, template_folder='project/templates')

@routes.route('/')
def hello():
    return "Hello World!"