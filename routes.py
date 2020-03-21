from flask import Blueprint, request
from flask_login import login_required, current_user
from project import db
from models import User, HelpRequest
from datetime import datetime

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

    # test if current user is a needy
    if not current_user.Needy:
        return {'message': 'Bad Request'}

    # fill the information of the new help 

    data['date'] = datetime.strptime(data['date'], '%d/%m/%Y %H:%M:%S')

    new_help = HelpRequest(
        id_volunteer=None, id_needy=current_user.id, date= data['date'], description=data['description']
        )

    # save the help in the database
    db.session.add(new_help)
    db.session.commit()

    return {'help_id': new_help.id}

@login_required
@routes.route('/accept_demand', methods=['POST'])
def accept_help_demand():
    """
        Receive the volunteer acceptance of a help
    """
    data = request.get_json()

    # find the help demand in the database

    help = HelpRequest.query.filter_by(id=data['help_id'])

    # fill the volunteer column with the volunteer id
    help.id_volunteer = data['volunteer_id']
    db.session.commit()

    return {'help_id': help.id}

@login_required
@routes.route('/accept_volunteer', methods=['POST'])
def accept_volunteer():
    """
        Receive the help offered by a volunteer and returns the help needed data
    """
    data = request.get_json()

    # find the help demand in the database
    help = HelpRequest.query.filter_by(id=data['help_id'])

    # assert if the volunteer column is not null
    if help.volunteer_id is None:
        return {'message': 'Bad Request'}

    # remove the help demand from the list
    help.status = 3
    db.session.commit()

    # return the contact info from the needy and volunteer
    volunteer = User.filter_by(id=help.id_volunteer)
    needy = User.filter_by(id=help.id_needy)

    contact_dict = {
        'volunteer': {
            'telephone': volunteer.telephone,
            'latitude': volunteer.latitude,
            'longitude': volunteer.longitude
        },
        'needy': {
            'telephone': needy.telephone,
            'latitude': needy.latitude,
            'longitude': needy.longitude
        }
    }

    return contact_dict