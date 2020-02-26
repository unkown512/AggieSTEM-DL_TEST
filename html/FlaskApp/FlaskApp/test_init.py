#Class Imports
from flask import Flask
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap

#Flask forms and login mods
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from wtforms import ValidationError
from flask_bootstrap import Bootstrap

#Model imports
from model import user_manager
import os


#DB Imports MysQL
import pymysql

#
from flask import request
from flask import render_template, redirect
from flask import url_for
from flask import send_file
from flask import flash

#Start flask app environment settings
app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = "3434hfhfh3b3g"

#TODO: Change hardcoded PW
db = pymysql.connect("localhost", "aggie", "Awsedrft22$", "aggiestemdl")


# Initlaize login_manager
def init_login_manager(app):
  login_manager = LoginManager()
  login_manager.init_app(app)
  login_manager.login_view = 'signin'
  user_list = list()
  return(login_manager, user_list)

(login_manager, user_list) = init_login_manager(app)

class User(UserMixin):
  def __init__(self, username, password, id, access):
    self.id = id
    self.username = username
    self.password = password
    self.access = access

  @staticmethod
  def get_user(user_id):
    for xuser in user_list:
      if(xuser.id == user_id):
        return xuser

  @staticmethod
  def remove_user(user_name):
    for xuser in user_list:
      if(xuser.username == user_name):
        user_list.remove(xuser)

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
  #TODO: Password length should be much longer than 80
  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
  remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
  #phone number
  username = StringField('Username <p class="text-info">First Initial + Last Name<p>'
    , validators=[InputRequired(), Length(min=4, max=15)])
  position = SelectField('Position', validators=[InputRequired()], choices=[('',''),('D','Director'),('S','Senior Doc'),('R','Researcher')])
  phone = StringField('Phone', validators=[InputRequired()])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
  conf_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80)])
  email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=250)])
  conf_email = StringField('Confirm Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=250)])
  privacy_agreement = SelectField('Privacy Policy: We collect users phone and email information for system notifications. Do you accept?', validators=[InputRequired()], choices=[('',''),('T','Yes'),('F','No')])
  contact_agreement = SelectField('Contact Policy: Admins can send out text messages or emails to users from the system. Do you wish to be contacted? ', validators=[InputRequired()], choices=[('',''),('T','Yes'),('F','No')])

# Get function for user during session
@login_manager.user_loader
def load_user(user_id):
  return User.get_user(str(user_id))

'''
  Starting of server routes and controller section of the application
  NOTE: @app.route defines a url case from the client, as follows: https://<ip>:<port>/<route>
'''

@app.route('/')
def hellow_world():
  return 'Hello, World! The Aggie STEM DL is currently down due to maintenance.. Please come back another time'

@app.route('/dashboard')
@login_required
def dashboard():
  return render_template("test_server.html")

# Login Page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = LoginForm()
  message = ""
  if(request.method == 'POST'):
    if(form.validate_on_submit()):
      user = form.username.data
      pw = form.password.data

      if(user_manager.validate_user(db, user, pw)):
        # Change user_profile to recno
        user_profile = user_manager.get_username_profile(db, user)
        user_access_level = user_manager.get_access_level(db, user)
        new_user = User(user, form.password.data, str(user_profile['_id']), user_access_level)
        user_list.append(new_user)
        login_user(new_user, remember=form.remember.data)
        return redirect(url_for('dashboard', user=current_user.username, access_level=current_user.access))
      else:
        message = "Incorrect username or password"
    else:
      message = ""
  elif(request.method == 'GET'):
    render_template("signin.html", form=form)
  return render_template("signin.html", form=form, error=message)

# Registration page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = RegisterForm()
  message = ""
  if(request.method == 'GET'):
    print("GET REQUEST");
    return render_template('signup.html', form=form)
  elif(request.method == 'POST'):
    if(form.validate_on_submit()):
      '''
        TODO MODEL TEAM: Update the 'add_user' function to
        insert into DB and create salts/hash/encryption for user etc...
        NOTE: TEMP_LOGIN_DB WILL BE REMOVED ONCE 'user_manager' is complete!!!
      '''
      print("POST REQUEST");
      #unique_number = ''  #'#' + str(random.randrange(10000)).zfill(4)
      smap = {'T': 1, 'F': 0} #statement
      user_data = [form.username.data, form.password.data, form.email.data, form.position.data, 
        form.phone.data, smap[form.privacy_agreement.data], smap[form.contact_agreement.data]]
      user_manager.add_user(db, user_data)

      message = "User: " + user_data[0] + " successfully created."
      return redirect(url_for('signin'))
    else:
      message = "Invalid Password or Email"
    print("POST REQUEST FAILED?");
  return render_template("signup.html", form=RegisterForm(), error=message)

# Recover Username Page
@app.route('/recov_username', methods=['GET', 'POST'])
def recov_username():
  form = ForgotUser()
  if(request.method == 'GET'):
    return render_template('recov_username.html', form=form)
  elif(request.method == 'POST'):
    return render_template('recov_username.html', form=form)
  else:
    return render_template('signin.html', form=form, error="TEST")

# Recover Password Page
@app.route('/recov_pw', methods=['GET', 'POST'])
def recov_pw():
  form = ForgotPw()
  if(request.method == 'GET'):
    return render_template('recov_pw.html', form=form)
  elif(request.method == 'POST'):
    email = form.email.data
    code = form.email.data

    f = open(APP_ROOT + "/data/code.txt", 'r+')
    curr_code = f.read()

    return render_template('recov_pw.html', form=form)
  else:
    return render_template('signin.html', form=form, error="TEST")

@app.route('/manage_users')
@login_required
def manage_users():
  return "HELLO"

@app.route('/manage_groups')
@login_required
def manage_groups():
  return "AYE"

@app.route('/message_users')
@login_required
def message_users():
  return "YE"

@app.route('/user_profile')
@login_required
def user_profile():
  return "up"

@app.route('/logout')
@login_required
def logout():
  return "WA"

if __name__ == "__main__":
  #IP = '128.194.140.214'
  #IP = '127.0.0.1'
  IP = '138.68.45.210'
  #app.run()
  app.run(host = os.getenv('IP',IP), port=int(os.getenv('PORT',5000)), debug=True)

