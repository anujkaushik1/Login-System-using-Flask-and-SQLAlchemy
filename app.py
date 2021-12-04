from enum import unique
from flask import Flask, render_template,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms import validators  #boolean field for checkbox
from wtforms.validators import InputRequired,Email,Length
from flask_sqlalchemy import SQLAlchemy   
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/ACER/Documents/Anuj/Python/Backend With Flask/Login System/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
Bootstrap(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
 

class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


@login_manager.user_loader
def load_user(user_id):     # it will take the user id and will return the specific user from the database based on the id
    return User.query.get(int(user_id))    # return the entire object for that user id like username, password, address etc



class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min = 4, max = 15)])
    password = StringField("password", validators=[InputRequired(),Length(min=8, max=80)])
    remember = BooleanField("remember")


class RegisterForm(FlaskForm):
    email = StringField("email",validators=[InputRequired(), Email(message="Invalid email"), Length(max=60)])
    username = StringField("username", validators=[InputRequired(), Length(min = 4, max = 15)])
    password = StringField("password", validators=[InputRequired(),Length(min=8, max=80)])

@app.route("/")
def index():
    return render_template("index.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)                            # it just logg in the user
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)



@app.route("/signup", methods=["GET","POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return "<h1> New User has been created </h1>"

        #return "<h1>" + form.email.data + " " + form.password.data + " " + form.email.data + "</h1>"
         

    return render_template("/signup.html", form = form)

@app.route("/dashboard")
@login_required            # cannot access the dashboard witout logging in (will redirect to login page)
def dashboard():
    return render_template("dashboard.html", name = current_user.username)



