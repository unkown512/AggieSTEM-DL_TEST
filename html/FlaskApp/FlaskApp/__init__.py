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

#DB Imports MysQL
import pymysql

#
from flask import request
from flask import render_template, redirect
from flask import url_for
from flask import send_file
from flask import flash

#
from datetime import datetime
import json
import ast
import random
import os
import smtplib, ssl
import boto3

#Start flask app environment settings
app = Flask(__name__)
Bootstrap(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#TODO: Change hardcoded PW
def db_client():
  try:
    db = pymysql.connect("localhost", "aggie", "Awsedrft22$", "aggiestemdl")
  except pymysql.Error as e:
    print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
    return False
  return db

# Initlaize login_manager
def init_login_manager(app):
  login_manager = LoginManager()
  login_manager.init_app(app)
  login_manager.login_view = 'signin'
  user_login_list = list()
  return(login_manager, user_login_list)

(login_manager, user_login_list) = init_login_manager(app)

class User(UserMixin):
  def __init__(self, username, password, id, access):
    self.id = id
    self.username = username
    self.password = password
    self.access = access

  @staticmethod
  def is_authenticated(self):
    return True

  @staticmethod
  def get_user(user_id):
    for xuser in user_login_list:
      if(xuser.id == user_id):
        return xuser

  @staticmethod
  def remove_user(user_name):
    for xuser in user_login_list:
      if(xuser.username == user_name):
        user_login_list.remove(xuser)

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=250)])
  #TODO: Password length should be much longer than 80
  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
  remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
  #phone number
  username = StringField('Username <p class="text-info">First Initial + Last Name<p>'
    , validators=[InputRequired(), Length(min=4, max=15)])
  position = SelectField('Position', validators=[InputRequired()], choices=[('',''),('R','Researcher')])
  phone = StringField('Phone', validators=[InputRequired()])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
  conf_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80)])
  email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=250)])
  conf_email = StringField('Confirm Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=250)])
  privacy_agreement = SelectField('Privacy Policy: We collect users phone and email information for system notifications. Do you accept?', validators=[InputRequired()], choices=[('',''),('T','Yes'),('F','No')])
  contact_agreement = SelectField('Contact Policy: Admins can send out text messages or emails to users from the system. Do you wish to be contacted? ', validators=[InputRequired()], choices=[('',''),('T','Yes'),('F','No')])

class ForgotUser(FlaskForm):
  email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=250)])

class newPw(FlaskForm):
  newpw = PasswordField('New Password', validators=[InputRequired(), Length(min=8, max=80)])
  conf_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80)])

class ForgotPw(FlaskForm):
  email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=250)])
  code = StringField('</br> Code', validators=[InputRequired(), Length(min=4, max=80)])


# Get function for user during session
@login_manager.user_loader
def load_user(user_id):
  print("load user")
  print(user_id)
  return User.get_user(int(user_id))

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
    return render_template("index.html", user=current_user.username, access_level = int(current_user.access))

# Login Page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = LoginForm()
  message = ""
  if(request.method == 'POST'):
    if(form.validate_on_submit()):
      email = form.email.data
      pw = form.password.data
      db = db_client()

      if(user_manager.validate_user(db, email, pw)):
        # Change user_profile to recno
        user_profile = user_manager.get_username(db, email)
        user_id = user_manager.get_user_id(db, user_profile)
        user_access_level = user_manager.get_access_level(db, str(user_id))
        new_user = User(user_profile, form.password.data, user_id, user_access_level)
        user_login_list.append(new_user)
        login_user(new_user, remember=form.remember.data)
        # Check if they have a /data/<DIR>, if not then create
        try:
          os.makedirs(APP_ROOT+"/static/data/"+str(user_id))
        except:
          print("Directory already exists for user = %s" % str(user_id))
        return redirect(url_for('dashboard'))
      else:
        message = "Incorrect username or password"
    else:
      message = ""
  elif(request.method == 'GET'):
    next_url = request.args.get("next")
    # TODO: Bug with user somehoe not being authenticated or is removed from user_login_list
    if(current_user.is_authenticated):
      if(next_url):
        if(len(next_url)>0):
          next_url = next_url[1:] #cannot have / in url_for
        return redirect(url_for(next_url))
    return render_template("signin.html", form=form)
  return render_template("signin.html", form=form, error=message)

@app.route('/upload_profile_image', methods=['POST'])
@login_required
def upload_profile_image():
  file_dir = APP_ROOT + '/static/data/' + str(current_user.id)
  print(file_dir)
  for user_file in request.files.getlist("file"):
    # Should be only one...
    print("GOT USER FILE")
    print(user_file)
    file_dest = file_dir + "/profile" 
    user_file.save(file_dest)
    break
  print("FILE SAVED")
  return redirect(url_for('user_profile')) 

# Registration page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = RegisterForm(request.form)
  message = ""
  if(request.method == 'GET'):
    return render_template('signup.html', form=form)
  elif(request.method == 'POST'):
    if(form.validate_on_submit()):
      '''
        TODO MODEL TEAM: Update the 'add_user' function to
        insert into DB and create salts/hash/encryption for user etc...
        NOTE: TEMP_LOGIN_DB WILL BE REMOVED ONCE 'user_manager' is complete!!!
      '''
      db = db_client()
      #unique_number = ''  #'#' + str(random.randrange(10000)).zfill(4)
      smap = {'T': 1, 'F': 0} #statement
      if(not user_manager.check_email(db, form.email.data) and not user_manager.check_phone_number(db, form.phone.data)):
        user_data = [form.username.data, form.password.data, form.email.data, form.position.data, 
          form.phone.data, smap[form.privacy_agreement.data], smap[form.contact_agreement.data]]
        user_manager.add_user(db, user_data)

        message = "User: " + str(form.username.data) + " successfully created."
        return redirect(url_for("signin"))
    else:
      message = "Invalid Data. TODO: MAKE SPECIFIC"
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
# Validate code and then open change password page
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

@app.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
  if(int(user_manager.get_access_level(db_client(), current_user.id)) < 2):
    return redirect(url_for('dashboard'))
  if(request.method == 'GET'):
    db = db_client()
    user_list = user_manager.get_all_users(db)
    temp = []
    for user in user_list:
      user_data = {}
      user_data['username'] = user[3] 
      user_data['uid'] = str(user[4])
      user_data['position'] = user[2]
      user_data['access_level'] = user[2]
      user_data['email'] = user[1]
      user_data['phone'] = user[0]
      user_data['groups'] = 'TODO'
      user_data['last_login'] = user[5].strftime("%Y-%M-%d @ %H:%M:%S")
      user_data['deleted'] = user[6] 
      temp.append(user_data)
    data = {}
    data['data'] = temp
    return render_template('manage_users.html', user=current_user.username, data=data,
      access_level = user_manager.get_access_level(db_client(), current_user.id))
  else:
    #POST
    db = db_client()
    post_args = json.loads(request.values.get("data"))
    user_id = next(iter(post_args['data']))
    if(post_args['action'] == "remove"):
      result = user_manager.delete_user(db, user_id)
      if(result == False):
        print("FAILED TO DELETE USER")
      return {}
    elif(post_args['action'] == "unremove"):
      #TODO?: Fix the post data setn to match others
      user_id = post_args['data']['uid']
      user_manager.update_user(db, user_id, {"deleted": "0"})
      return {}
    else:
      response_data = {}
      response_data['data'] = []
      post_args['data'][user_id]['uid'] = user_id
      response_data['data'].append(post_args['data'][user_id])

      new_user_data = {}
      new_user_data['access_level'] = int(response_data['data'][0]['access_level'])
      new_user_data['position'] = response_data['data'][0]['position']

      user_manager.update_user(db, user_id, new_user_data)
      return response_data
      

@app.route('/manage_groups')
@login_required
def manage_groups():
  return "AYE"

@app.route('/message_users')
@login_required
def message_users():
  db = db_client()
  if(int(user_manager.get_access_level(db, current_user.id)) < 2):
    return redirect(url_for('dashboard'))
  elif(request.method == 'GET'):
    message_user_list = user_manager.get_all_users(db)
    groups = ["Camp A", "Camp B", "Camp C", "Camp D"]
    temp = []
    i = 0
    for row in message_user_list:
      user_data = {}
      user_data['uid'] = str(row[4])
      user_data['username'] = row[3]
      user_data['phone'] = row[0]
      user_data['groups'] = groups[i] #Make sure it works with multigroups/user
      temp.append(user_data)
      i += 1
      if(i>3):
        i=0
    data = {}
    data['data'] = temp

    return render_template('message_users.html', user=current_user.username, data = data, groups = list(groups),
      access_level=user_manager.get_access_level(db_client(), current_user.id))
  elif(request.method == 'POST'):
    return render_template('message_users.html', user=current_user.username, access_level=current_user.access)
  return render_template('index.html', user=current_user.username, error="TEST", 
      access_level=user_manager.get_access_level(db_client(), current_user.id))

@app.route('/request_data_from', methods=['GET', 'POST'])
@login_required
def request_data_form():
  if(request.method == 'GET'):
    # Load new form
    return render_template('request_data_form.html')
  elif(request.method == 'POST'):
    # Get form data
    print("Get form data..WTF")
    # Change to just loop through request form...
    data = {}
    for id_name in request.form:
      data[id_name] = request.form[id_name]
      print(id_name + ", " + data[id_name])

    print("calling redirect....")
    return redirect(url_for('user_profile'))

@app.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
  if(request.method == 'GET'):
    db = db_client()
    if(str(request.args.get('type')) == "1"):
      user_id = request.args.get('user')
    else:
      user_id = current_user.id
    userdata = user_manager.get_user_profile(db, str(user_id))
    
    if(userdata):
      username = userdata['username']
      phonenumber = userdata['phone']
      email = userdata['email']
      position = userdata['position']
      position_map = {'3': "Director", '2': "Senior Doc", '1': "Researcher"}
      position = position_map.get(position, 0)

      return render_template('user_profile.html', user=username, email=email, 
        phonenumber=phonenumber, position=position, 
        profile_img="static/data/"+str(user_id)+"/profile",
        user_links = user_manager.get_profile_ahref_links(db, str(user_id)),
        access_level = user_manager.get_access_level(db_client(), current_user.id))
  elif(request.method=='POST'):
    data = {}
    return render_template('user_profile.html', data=data)
    
  return redirect(url_for('dashboard')) 

@app.route('/logout')
@login_required
def logout():
  User.remove_user(current_user.username)
  logout_user()
  return redirect(url_for('signin'))

@app.route('/send_sms', methods=['GET','POST'])
@login_required
def send_sms():
  if(int(user_manager.get_access_level(db_client(), current_user.id)) < 2):
    return redirect(url_for('dashboard'))

  if(request.method == 'GET'):
    print("do something")
  elif(request.method == 'POST'):
    numbers = ast.literal_eval(request.form['numbers'])
    message = request.form['message'][1:-1]
    print("SEND MESSAGE")
    print(numbers)
    print(message)

    f = open("/home/aggie/.aws/credentials", "rt")
    data = f.read().split("\n")
    client = boto3.client(
        'sns',
        aws_access_key_id= data[1].split("=")[1].lstrip(),
        aws_secret_access_key= data[2].split("=")[1].lstrip(),
        region_name="us-east-1")

    print(data[1].split("=")[1].lstrip())
    print(data[2].split("=")[1].lstrip())
    topic = client.create_topic(Name="message")
    topic_arn = topic['TopicArn']

    for num in numbers:
      client.subscribe(TopicArn=topic_arn, Protocol='sms', Endpoint="+1" + num)

    client.publish(Message = "Aggie STEM DL: \n\n" + message, TopicArn=topic_arn)

    for sub in client.list_subscriptions()['Subscriptions']:
      client.unsubscribe(SubscriptionArn=sub['SubscriptionArn'])
    client.delete_topic(TopicArn=topic_arn)
    print("Message Sent")
    #flash("Message sent") # Doesnt work
  return("testing") 

# Get email code
@app.route('/send_email_code', methods=['POST'])
def send_email_code():
  if(request.method == 'GET'):
    print("ERROR -- INVALID GET REQUEST")
  elif(request.method == 'POST'):
    print("TRYING TO SEND EMAIL")
    # emailmsg
    # txtmsg

    data = request.form.to_dict()

    for var in data:
      email = var.split("\"email\":\"")
      email = email[1].split("\"")
      email = email[0]
      message = var.split("\"message\":\"")
      message = message[1].split("\"")
      message = message[0]


    code = random.getrandbits(64)
    f = open(APP_ROOT + "/data/code.txt", 'r+')
    f.write(str(code))
    f.close()
    message = message + ": " + str(code)

    f = open("/home/aggie/.smtp/credentials", "rt")
    data = f.read().split("\n")
    password = data[1].split("=")[1].lstrip()
    port = data[2].split("=")[1].lstrip()
    sender = data[0].split("=")[1].lstrip()

    context = ssl.create_default_context()
    reciever = email
    smtp_server = "smtp.gmail.com"


    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
      server.login(sender, password)
      server.sendmail(sender, reciever, message)
  return("EMAIL SENT")

# Send Emails
@app.route('/send_email', methods=['POST'])
@login_required
def send_email():
  if(request.method == 'GET'):
    print("ERROR -- INVALID GET REQUEST")
    return redirect(url_for('dashboard'))
  elif(request.method == 'POST'):
    print("TRYING TO SEND EMAIL")
    # emailmsg
    # txtmsg
    email = request.form['email']
    message = request.form['message'][1:-1]

    f = open("/home/aggie/.smtp/credentials", "rt")
    data = f.read().split("\n")
    password = data[1].split("=")[1].lstrip()
    port = data[2].split("=")[1].lstrip()


    context = ssl.create_default_context()
    sender = data[0].split("=")[1].lstrip()
    reciever = email
    smtp_server = "smtp.gmail.com"


    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
      server.login(sender, password)
      server.sendmail(sender, reciever, message)
    return("EMAIL SENT")

@app.route('/table_reload', methods=['GET', 'POST'])
@login_required
def table_reload():
  db = db_client()
  user_list = user_manager.get_all_users(db)
  temp = []
  for user in user_list:
    user_data = {}
    user_data['username'] = user[3]
    user_data['uid'] = str(user[4])
    user_data['position'] = user[2]
    user_data['access_level'] = user[2]
    user_data['email'] = user[1]
    user_data['phone'] = user[0]
    user_data['groups'] = 'TODO'
    user_data['last_login'] = user[5].strftime("%Y-%M-%d @ %H:%M:%S")
    user_data['deleted'] = user[6]
    temp.append(user_data)
  data = {}
  data['data'] = temp
  return data

