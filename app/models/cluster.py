from .base import Audit
from app.helpers import parse_to_dict
from app import db


class Cluster(Audit):
    __tablename__ = 'clusters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return parse_to_dict(self)

    def __repr__(self):
        return '<Cluster {0}>'.format(self.username)
