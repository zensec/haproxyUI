from .base import Audit
from app.helpers import parse_to_dict
from app import db


class Upstream(Audit):
    __tablename__ = 'upstreams'
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'))
    ip_address = db.Column(db.String(100))
    port = db.Column(db.Integer)

    def __repr__(self):
        return 'Upstream {0} for domain {1]>'.format(self.ip_address, self.domain.name)

    def to_dict(self):
        return parse_to_dict(self)
