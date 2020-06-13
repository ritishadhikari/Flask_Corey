import os
class Config:

    # For the flask forms
    #SECRET_KEY=os.environ.get('SECRET_KEY')
    SECRET_KEY='9afc0b089983209aa62baa698790a4a0'
    # For the Purpose of setting up the Database
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'

    # For the Purpose of Setting up Mail Service for Password
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    #MAIL_USERNAME=os.environ.get('EMAIL_USER')
    MAIL_USERNAME='ritishadhikari'
    #MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    MAIL_PASSWORD='stratosphere'
