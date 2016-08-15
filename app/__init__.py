from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand
import flask_login

app = Flask(__name__)
app.config.from_object('config.BaseConfig')

db = SQLAlchemy(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host="0.0.0.0", port=app.config['PORT']))


def do_imports(flask_app):
    from .imports import register_blueprints
    register_blueprints(flask_app)

do_imports(app)
