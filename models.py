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

    def __init__(self,name,telephone,email,password,volunteer,needy,longitude,latitude,role):
        """Constructor"""

        self.nome = clean(nome)
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

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    # def is_anonymous(self):
    #     """False, as anonymous users aren't supported."""
    #     return Falsed

    def addUser(name,tel,email,password,role):
        
        user = User(name,tel,email,password,role)
        
        db.session.add(user)
        db.session.commit()

        return user
    def researchNeedy(busca=''):
        """ Return every needy person """

        if research == '':
            needy = User.query.filter_by(needy=True).all()

            return needy
    
    def userId(id_user):
        """ Return information about the user by the id """

        information = User.query.filter_by(id=id_user).first()

        return information
    
class helpRequest(db.Model):
    """ Class specif for help request """

    id = db.Column(db.Integer, primary_key = True)
    id_volunteer = db.Column(db.Integer, ForeignKey("user.id"))
    id_needy = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    data = db.Column(db.DateTime)
    description = db.Column(db.Text) #audio or text

    #__table_args__ = (UniqueConstraint('id_needy', name='unic_request'),)

    def __init__(self, id_aluno, id_bolsa, data, anexo):
        """Constructor."""
        self.id_aluno = id_aluno
        self.id_bolsa = id_bolsa
        self.data = data
        self.anexo = anexo

        aluno = Usuario.query.filter_by(id=id_aluno).first()
        bolsa = Bolsa.query.filter_by(id=id_bolsa).first()
        prof = Usuario.query.filter_by(id=bolsa.prof_id).first()

        # Enviando email para professor com dados da inscrição
        self.emailDadosInscricao(aluno,bolsa)

    def emailDadosInscricao(self, aluno, bolsa, prof):
        """Envia email com dados de inscrição para professor"""
        port = 465  # For SSL
        password = 'bolsas@123'

        sender_email = "bolsasufjf@gmail.com"
        receiver_email = prof.email
        subject = f"Candidatura da bolsa mamofaf"
        body = f"""\
        Aluno: {aluno.nome} {aluno.sobrenome}
        
        Matricula: {aluno.matricula}
        Curso: {aluno.curso}
        E-mail: {aluno.email}
        """

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = self.anexo

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=curriculo.pdf",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

    def buscarInscricoes(busca=''):
        """ Retorna todas as inscricoes relacionadas a busca """

        if busca == '':
            inscricoes = InscricaoBolsa.query.filter_by(InscricaoBolsa.id_bolsa).all()

        return inscricoes

    def buscaInscricaoAluno(aluno_id):

        inscricao = InscricaoBolsa.query.filter_by(id_aluno=aluno_id).all()

        return inscricao

    def buscaNome(inscricoes):
        bolsa = []
        for inscricao in inscricoes:
            bolsa.append(Bolsas.getBolsas(inscricoes.id_bolsa))

        return bolsa