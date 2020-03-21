from project import db
from bleach import clean
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
  
    "Control class of application user"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    telephone = db.Column(db.String(20), unique = True)
    email = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(20))
    volunteer = db.Column(db.Boolean)
    needy = db.Column(db.Boolean)
    longitude = db.Column(db.FLOAT(15,10)) #longitude coordenates
    latitude = db.Column(db.FLOAT(15,10)) #latitude coordenate

    def __init__(self,name,telephone,email,password,longitude,latitude,role):
        """Constructor"""

        self.name = clean(name)
        self.telephone = clean(telephone)
        self.email = clean(email)
        self.password = clean(password)
        self.longitude = clean(longitude)
        self.latitude = clean(latitude)
        self.volunteer = role == 'Volunteer'
        self.needy = role == 'Needy'

    @staticmethod
    def addUser(name,telephone,email,password,longitude,latitude,role):
        
        user = User(name,telephone,email,password,longitude,latitude,role)
        
        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def researchNeedy():
        """ Return every needy person """

        needy = User.query.filter_by(needy=True).all()

        return needy
    
    @staticmethod
    def userId(id_user):
        """ Return information about the user by the id """

        information = User.query.filter_by(id=id_user).first()

        return information

    @staticmethod
    def getUserByEmail(email):
        """ Return user by email """
        
        user = User.query.filter_by(email=email).first()

        return user
    
class HelpRequest(db.Model):
    """ Class specif for help request """

    id = db.Column(db.Integer, primary_key = True)
    id_volunteer = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_needy = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime)
    description = db.Column(db.Text) #audio or text
    status = db.Column(db.Integer)

    def __init__(self, id_needy, date, description):
        """Constructor."""
        self.id_needy = id_needy
        self.date = date
        self.description = description
        self.status = 0

    def addHelpRequest(self, id_needy, date, description):
        new_help = HelpRequest(id_needy, date, description)
        
        db.session.add(new_help)
        db.session.commit()

        return new_help