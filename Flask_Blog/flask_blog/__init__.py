from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)
app.config['SECRET_KEY']='9afc0b089983209aa62baa698790a4a0'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app=app)
bcrypt=Bcrypt(app=app)
login_manager=LoginManager(app=app)

#Telling the login manager what is the login view
login_manager.login_view='login'
login_manager.login_message = "To Access this Page, you must Login"
login_manager.login_message_category='info'


#importing the routes.py file after importing the app in __init__.py file
from flask_blog import routes
