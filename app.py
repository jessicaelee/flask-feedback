from flask import Flask, render_template, redirect, session, flash
from models import db, bcrypt, connect_db, User, Feedback
from forms import RegisterUser, LoginUser, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
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

        if new_user:
            db.session.add(new_user)
            db.session.commit()
            session["username"] = new_user.username  # keep logged in
            return redirect(f'/users/{username}')

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
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)

@app.route('/users/<username>')
def show_secret(username):
    """if user is logged in, show "You made it!"""

    if "username" not in session or session['username'] != username:
        # flash("You must be logged in to view!")
        return redirect("/")

    user = User.query.get_or_404(username)
    feedback = Feedback.query.filter_by(username_fk=user.username).all()
    return render_template("user_detail.html", user=user, feedback=feedback)

@app.route('/logout')
def logout_user():
    """Logs user out and redirects to homepage."""

    session.pop("username")

    return redirect("/")

@app.route('/users/<username>/delete', methods=['POST'])
def remove_users_and_feedback(username):
    """remove user from db and delete all their feedback"""
     
    if "username" not in session:
        # flash("You must be logged in to view!")
        return redirect("/")

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """display a form to add feedback and post feedback"""

    if "username" not in session:
        # flash("You must be logged in to view!")
        return redirect("/")

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username_fk=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    
    return render_template("add_feedback.html", form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """display a form to edit feedback and post feedback"""

    if "username" not in session:
        # flash("You must be logged in to view!")
        return redirect("/")

    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback.title = title
        feedback.content = content 
        db.session.commit()
        return redirect(f'/users/{feedback.username_fk}')
    
    return render_template("update_feedback.html", form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """delete a feedback post"""

    if "username" not in session:
        # flash("You must be logged in to view!")
        return redirect("/")

    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username_fk
    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{username}")