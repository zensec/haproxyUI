from app.helpers import parse_to_dict
from .base import Audit
from app import db


class Domain(Audit):
    __tablename__ = 'domains'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'))

    def __repr__(self):
        return '<Domain {0}>'.format(self.name)

    def to_dict(self):
        return parse_to_dict(self)
