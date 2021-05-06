from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5433/feedback_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secretkey123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def show_home_page():
    """renders the homepage"""
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User.register(
            username = form.username.data, 
            password = form.password.data,
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect("/secret")

    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(
            username = form.username.data,
            password = form.password.data
        )
        if user:
            return redirect("/secret")
        else:
            form.username.errors = ["Invalid Username/Password"]

    return render_template("login.html", form=form)



@app.route('/secret')
def show_secret():
    return render_template("secret.html")