from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config


# For the Purpose of setting up the Database
db=SQLAlchemy()

# For the purpose of setting up the hashing passwords
bcrypt=Bcrypt()

# For the Purpose of User Login
login_manager=LoginManager()
#Telling the login manager what is the login view
login_manager.login_view='users.login'
login_manager.login_message = "To Access this Page, you must Login"
login_manager.login_message_category='info'

# For the Purpose of Setting up Mail Service for Password
mail=Mail()


def create_app(config_class=Config):

    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    #importing the routes.py file after importing the app in __init__.py file
    from flask_blog.users.routes import users
    from flask_blog.main.routes import main
    from flask_blog.posts.routes import posts
    from flask_blog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app
