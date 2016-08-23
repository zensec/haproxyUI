from werkzeug.security import generate_password_hash, check_password_hash
from .base import Audit
from app.helpers import parse_to_dict
from app import db


class User(Audit):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    name = db.Column(db.String(100))
    hash = db.Column(db.String(500))
    last_seen = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=False)

    def to_dict(self):
        resp = parse_to_dict(self)
        del resp['hash']
        return resp

    def encrypt_password(self, password):
        self.hash = generate_password_hash(password)

    def validate_password(self, password):
        if check_password_hash(self.hash, password):
            return True
        return False

    def __repr__(self):
        return '<User {0}>'.format(self.username)
