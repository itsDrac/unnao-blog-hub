import os

DEBUG = True
SQLALCHEMY_DATABASE_URI ='sqlite:///database.db'
SECRET_KEY = '1b49b02d90b26cddba45d123458e690a'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('EMAIL')
MAIL_PASSWORD = os.environ.get('EMAIL_PASS')