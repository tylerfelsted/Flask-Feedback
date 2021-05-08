from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Encrypts the password for storage, and then creates a returns a new user object with the information provided"""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')
        return cls(username=username, password=hashed, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Checks the username and password provided against the username and password stored in the database"""
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))
    user = db.relationship('User', backref=backref('feedback', cascade="all,delete"))