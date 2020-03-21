from flask import Blueprint, request
from flask_login import login_required, current_user
from project import db
from models import User, HelpRequest
from datetime import datetime
import numpy as np

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
    data = request.get_json()
    list_needy = HelpRequest.query.id_needy

    long_needy = []
    lat_needy = []
    for num in range(len(list_needy)-1):
        long_needy.append(User.query.filter_by(id=list_needy[num]).longitude) 
        lat_needy.append(User.query.filter_by(id=list_needy[num]).latitude)

    long_volunteer, lat_volunteer = User.coordenatesById(data.id_volunteer)

    distance = []
    for num in range(len(long_needy)):
        distance.append(calculateDistance(long_needy[num],lat_needy[num],long_volunteer,lat_volunteer))
    dic = {}
    for num in range(len(list_needy)-1):
        dic[list_needy[num]] = distance[num]
    order = sorted(dic.items(), key=itemgetter(1))
    result = []
    for num in range(len(order)-1):
        description = HelpRequest.descriptionByNeedy(order[0][num])
        result.append({'id_needy':order[0][num], 'distance':order[1][num], 'description':description})

    return result

    
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