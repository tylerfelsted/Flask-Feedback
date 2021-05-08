from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegistrationForm, LoginForm, FeedbackForm

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
    """redirects to the registration page"""
    if 'username' not in session:
        return redirect('/register')
    else:
        return redirect(f'/users/{session["username"]}')

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
        session['username'] = new_user.username
        return redirect(f"/users/{new_user.username}")

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
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid Username/Password"]

    return render_template("login.html", form=form)
        
@app.route('/logout')
def logout_user():
    session.pop('username')
    return redirect('/')

@app.route("/users/<username>")
def show_user_details(username):
    if 'username' not in session:
        flash("Please login or register first")
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        return render_template("user_details.html", user=user)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if 'username' not in session:
        return redirect('/')
    elif session['username'] == username:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash(f'{username} deleted')
        return redirect('/')
    else:
        flash("Not authorized to delete this user")
        return redirect('/')


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def show_add_feedback_form(username):
    if session.get('username') == username:
        form = FeedbackForm()
        if form.validate_on_submit():
            user = User.query.get_or_404(username)
            feedback = Feedback(
                title = form.title.data,
                content = form.content.data,
                user = user
            )
            db.session.add(feedback)
            db.session.commit()
            flash("Feedback added")
        else:
            return render_template("feedback_form.html", form=form)
    else:
        flash("User is not authorized to add feedback")
    return redirect('/')