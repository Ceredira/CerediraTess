import os

BASEDIR = os.environ.get('CT_BASEDIR') or os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CSRF_ENABLED = True
    DEBUG = bool(os.environ.get('CT_DEBUG')) if os.environ.get('CT_DEBUG') else False
    FLASK_ADMIN_SWATCH = 'flatly'
    SECRET_KEY = os.environ.get('CT_SECRET_KEY') or 'mysecret'
    SERVER_CERT = os.environ.get('CT_SERVER_HTTPS_CERT') or None
    SERVER_HOST = os.environ.get('CT_SERVER_HOST') or '0.0.0.0'
    SERVER_HTTPS = bool(os.environ.get('CT_SERVER_HTTPS')) or False
    SERVER_KEY = os.environ.get('CT_SERVER_HTTPS_KEY') or None
    SERVER_PORT = int(os.environ.get('CT_SERVER_PORT')) if os.environ.get('CT_SERVER_PORT') else 7801
    SQLALCHEMY_DATABASE_URI = os.environ.get('CT_DATABASE_URL') or f'sqlite:///{BASEDIR}\\CerediraTess.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
