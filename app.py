from flask import Flask, request, jsonify, render_template, redirect
from models import db, connect_db, User
from forms import AddUser, LoginUser

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

    form = AddUser()
    return "hello"

    # if form.validate_on_submit():


    # else:
    #     return render_template("register.html", form=form)

# @app.route('/login' methods=['GET', 'POST')
# def login_user():
#     """process the login form and make sure user is authenticated, redirect to secret"""

#     form = LoginUser()

#     if form.validate_on_submit():

#     else:
#         return render_template("login.html", form=form)

# @app.route('secret')
# def show_secret():
#     """if user is logged in, show "You made it!"""

#     return render_template("secret.html")