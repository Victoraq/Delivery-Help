from project import db
from bleach import clean
from flask_sqlalchemy import SQLAlchemy


import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class User(db.Model):
  
    "Control class of application user"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    telephone = db.Column(db.Text, unique = True)
    email = db.Column(db.Text, unique = True)
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

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_email(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def addUser(self, name,tel,email,password,role):
        
        user = User(name,tel,email,password,role)
        
        db.session.add(user)
        db.session.commit()

        return user

    def researchNeedy(self, busca=''):
        """ Return every needy person """

        if research == '':
            needy = User.query.filter_by(needy=True).all()

            return needy
    
    def userId(self, id_user):
        """ Return information about the user by the id """

        information = User.query.filter_by(id=id_user).first()

        return information

    def getUserByEmail(self, email):
        """ Return user by email """
        
        user = User.query.filter_by(email=email).first()

        return user
    
class HelpRequest(db.Model):
    """ Class specif for help request """

    id = db.Column(db.Integer, primary_key = True)
    id_volunteer = db.Column(db.Integer, ForeignKey("user.id"))
    id_needy = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime)
    description = db.Column(db.Text) #audio or text

    #__table_args__ = (UniqueConstraint('id_needy', name='unic_request'),)

    def __init__(self, id_needy, date, description):
        """Constructor."""
        self.id_needy = id_needy
        self.date = date
        self.description = description

        needy = User.query.filter_by(role='Needy').first()

        # # Enviando email para professor com dados da inscrição
        # self.emailDadosInscricao(aluno,bolsa)

    
    def researchRequest(research=''):
        """ Return every help request """

        if research == '':
            request = helpRequest.query.filter_by(helpRequest.id).all()

        return request

    