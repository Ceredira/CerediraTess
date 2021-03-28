import os

import bleach as bleach

BASEDIR = os.environ.get('CT_BASEDIR') or os.path.abspath(os.path.dirname(__file__))
print(f'CerediraTess BASEDIR: {BASEDIR}')


class Config(object):

    def uia_username_mapper(identity):
        # we allow pretty much anything - but we bleach it.
        return bleach.clean(identity, strip=True)

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

    ################
    # Flask-Security-Too
    ################

    # URLs
    SECURITY_LOGIN_URL = "/login"
    SECURITY_LOGOUT_URL = "/logout"
    SECURITY_POST_LOGIN_VIEW = "/"
    SECURITY_POST_LOGOUT_VIEW = "/"
    SECURITY_POST_REGISTER_VIEW = "/"

    # Включает регистрацию
    SECURITY_REGISTERABLE = False
    SECURITY_REGISTER_URL = "/register"
    SECURITY_SEND_REGISTER_EMAIL = False

    # Включет сброс пароля
    SECURITY_RECOVERABLE = True
    SECURITY_RESET_URL = "/reset"
    SECURITY_SEND_PASSWORD_RESET_EMAIL = False

    # Включает изменение пароля
    SECURITY_CHANGEABLE = True
    SECURITY_CHANGE_URL = "/change"
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False

    SECURITY_USER_IDENTITY_ATTRIBUTES = [{"username": {"mapper": uia_username_mapper, "case_insensitive": True}}]
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = os.environ.get('CT_SECURITY_PASSWORD_SALT') or '210853635775369807482681431501385084239'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
