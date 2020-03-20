from flask import Blueprint

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return "Welcome to the Delivery Help"

# Return the help board list
@routes.route('/helpboard', methods=['GET'])
def helpboard():
    return []

@routes.route('/accept_demand', methods=['POST'])
def accept_demand():
    return NotImplemented

@routes.route('/accept_volunteer', methods=['POST'])
def accept_volunteer():
    return NotImplemented