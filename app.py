from flask import Flask, render_template, redirect, session, flash
from models import db, bcrypt, connect_db, User
from forms import RegisterUser, LoginUser

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flaskfeedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "sekrit key"

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """redirect to register page"""
    
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """show and process registration form and add new user"""

    form = RegisterUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/secret')

    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """process the login form and make sure user is authenticated, redirect to secret"""

    form = LoginUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        login_user = User.authenticate(username, password)

        if login_user:
            session["username"] = login_user.username  # keep logged in
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)

@app.route('/secret')
def show_secret():
    """if user is logged in, show "You made it!"""

    return render_template("secret.html")