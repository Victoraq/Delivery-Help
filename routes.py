from flask import Blueprint, request
from flask_login import login_required, current_user
from project import db, login_manager
from models import User, HelpRequest
from datetime import datetime
import json

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return "Welcome to the Delivery Help!"

@login_required
@routes.route('/helpboard', methods=['GET'])
def helpboard():
    """
        Return the help board list
    """
    # get from the database the help demands
    # calculates the distance from the person to the demands
    # order the list by the distance
    # return the demand list
    return json.dumps([])

@login_required
@routes.route('/new_help', methods=['POST'])
def new_help():
    """
        Receive the new help and put it in the database
    """
    data = request.get_json()

    print(current_user.is_authenticated)

    # test if current user is a needy
    if not current_user.needy:
        return json.dumps({'message': 'Bad Request'})

    # fill the information of the new help 

    data['date'] = datetime.strptime(data['date'], '%d/%m/%Y %H:%M:%S')

    new_help = HelpRequest(
        id_needy=current_user.id, date=data['date'], description=data['description']
        )

    # save the help in the database
    db.session.add(new_help)
    db.session.commit()

    return json.dumps({'help_id': new_help.id})

@login_required
@routes.route('/accept_demand', methods=['POST'])
def accept_help_demand():
    """
        Receive the volunteer acceptance of a help
    """
    data = request.get_json()

    # find the help demand in the database
    help = HelpRequest.query.filter_by(id=int(data['help_id'])).first()

    # verify if is a volunteer
    if not current_user.volunteer:
        return {'message': 'Bad Request'}

    # fill the volunteer column with the volunteer id
    help.id_volunteer = current_user.id
    help.status = 1
    db.session.commit()

    return json.dumps({'help_id': help.id})

@login_required
@routes.route('/accept_volunteer', methods=['POST'])
def accept_volunteer():
    """
        Receive the help offered by a volunteer and returns the help needed data
    """
    data = request.get_json()

    # find the help demand in the database
    help = HelpRequest.query.filter_by(id=int(data['help_id'])).first()

    # assert if is a needy
    if not current_user.needy:
        return json.dumps({'message': 'Not a needy user'})

    # assert if is the help owner
    if current_user.id != help.id_needy:
        return json.dumps({'message': 'Not the owner'})

    # assert if the volunteer column is not null
    if help.id_volunteer is None:
        return json.dumps({'message': 'Bad Request'})

    # remove the help demand from the list
    help.status = 3
    db.session.commit()

    # return the contact info from the needy and volunteer
    volunteer = User.query.filter_by(id=help.id_volunteer).first()
    needy = User.query.filter_by(id=help.id_needy).first()

    contact_dict = {
        'volunteer': {
            'telephone': volunteer.telephone,
            'latitude': str(volunteer.latitude),
            'longitude': str(volunteer.longitude)
        },
        'needy': {
            'telephone': needy.telephone,
            'latitude': str(needy.latitude),
            'longitude': str(needy.longitude)
        }
    }

    print(contact_dict)

    return json.dumps(contact_dict)