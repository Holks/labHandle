import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') \
        or b""""""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('MDL_ADMIN')
    LANGUAGES = ['en', 'es']
    POSTS_PER_PAGE = 25
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    UNCERTAINTY_FOLDER = os.environ.get('UNCERTAINTY_FOLDER')
    ALLOWED_FILE_EXTENSIONS = set(['txt', 'pdf', 'png', \
        'jpg', 'jpeg', 'gif', 'xlsx',])
    PROTOCOL_EXTENSIONS = set(['xlsx'])
    UNCERTAINTY_EXTENSIONS = set(['xlsx','txt'])
    MOIS_API = ''
