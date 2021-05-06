from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

class RegistrationForm(FlaskForm):
    """Form used to register a new user"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form used to login and existing user"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
