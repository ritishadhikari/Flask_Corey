import os

# For the Purpose of setting up the Database
print(os.environ.get('SQLALCHEMY_DATABASE_URI'))

# For the Purpose of Setting up Mail Service for Password
print(os.environ.get('MAIL_SERVER'))
print(os.environ.get('MAIL_PORT'))
print(os.environ.get('MAIL_USE_TLS'))
print(os.environ.get('EMAIL_USER'))
print(os.environ.get('EMAIL_PASSWORD'))
