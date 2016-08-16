from app.helpers import parse_to_dict
from .base import Audit
from app import db


class Server(Audit):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'))

    name = db.Column(db.String(100))
    ip_address = db.Column(db.String(15))
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Server {0}>'.format(self.name)

    def to_dict(self):
        return parse_to_dict(self)

