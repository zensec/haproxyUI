from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Server, Manager
from flask_modus import Modus
from app.helpers import PyCrypto247
from flask_migrate import Migrate, MigrateCommand
from urllib.parse import unquote

app = Flask(__name__)
app.config.from_object('config.BaseConfig')

db = SQLAlchemy(app)
enc = PyCrypto247(app.config['PASSWORD_ENCRYPTION_KEY'])

modus = Modus(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host="0.0.0.0", port=app.config['PORT']))


@manager.command
def list_routes():
    """Lists all routes known to this application"""
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)
    for line in sorted(output):
        print(line)


@manager.command
def create_user(username=None, password=None):
    from werkzeug.security import generate_password_hash
    """Creates a new user in the database"""
    if not username or not password:
        return 'Please specify username & password'
    from app.models.user import User
    user = User.query.filter_by(username=username).first()
    if user:
        return 'Username already in use'
    user = User(username=username, name=username, is_active=True, hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    return 'User created successfully'


def do_imports(flask_app):
    from .imports import register_blueprints
    register_blueprints(flask_app)

do_imports(app)
db.create_all()