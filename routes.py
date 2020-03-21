from flask import Blueprint, request
from flask_login import login_required, current_user
from project import db
from models import User, HelpRequest
from datetime import datetime
import json
import numpy as np
import math
from operator import itemgetter

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
    list_help = HelpRequest.query.all()

    long_needy = []
    lat_needy = []
    for help in list_help:
        long_needy.append(User.query.filter_by(id=help.id_needy).first().longitude)
        lat_needy.append(User.query.filter_by(id=help.id_needy).first().latitude)

    long_volunteer, lat_volunteer = User.coordenatesById(current_user.id)

    distance = []
    for num in range(len(long_needy)):
        distance.append(calculateDistance(long_needy[num],lat_needy[num],long_volunteer,lat_volunteer))
    dic = {}
    for num in range(len(list_help)):
        dic[list_help[num]] = distance[num]
    order = sorted(dic.items(), key=itemgetter(1))
    result = []
    for num in range(len(order)):
        description = HelpRequest.descriptionByNeedy(order[num][0].id_needy)
        result.append({'id_needy':order[num][0].id_needy, 'distance':order[num][1], 'description':description})

    return json.dumps(result)


def calculateDistance(long1,lat1,long2,lat2):
    R = 6373.0
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    lat2 = math.radians(lat2)
    long2 = math.radians(long2)

    dlon = long2 - long1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

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

    return json.dumps(contact_dict)