class BaseConfig(object):
    PORT = 3000
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    PASSWORD_ENCRYPTION_KEY = 'A16DigitSecureStringHere'
    SECRET_KEY = 'ASecretKeyHere'

    RELEASE_VERSION = 'Development v0.1'
    RELEASE_DATE = '00/00/0000'
