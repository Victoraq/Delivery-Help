from flask import Blueprint, request
from flask_login import login_required, current_user

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return "Welcome to the Delivery Help!"

@routes.route('/helpboard', methods=['GET'])
def helpboard():
    """
        Return the help board list
    """
    # get from the database the help demands
    # calculates the distance from the person to the demands
    # order the list by the distance
    # return the demand list
    return []


@login_required
@routes.route('/new_help', methods=['POST'])
def new_help():
    """
        Receive the new help and put it in the database
    """
    data = request.get_json()

    # test if current user is a need
    # get the user data from the database
    # fill the information of the new help 
    # send to the database
    # return the id of the new help

    return NotImplemented

@login_required
@routes.route('/accept_demand', methods=['POST'])
def accept_help_demand():
    """
        Receive the volunteer acceptance of a help
    """

    data = request.get_json()

    help_id = data['help_id']
    volunteer_id = data['volunteer_id']

    # find the help demand in the database
    # fill the volunteer column with the volunteer id

    return NotImplemented

@login_required
@routes.route('/accept_volunteer', methods=['POST'])
def accept_volunteer():
    """
        Receive the help offered by a volunteer and returns the help needed data
    """

    data = request.get_json()

    help_id = data['help_id']

    # assert if the volunteer column is not null
    # remove the help demand from the list
    # return the contact info from the needed

    return NotImplemented