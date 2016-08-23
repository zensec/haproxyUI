from app import db
from app.helpers import parse_to_dict


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer)
    action = db.Column(db.String(100))
    audit_created_on = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return parse_to_dict(self)

    def create(self):
        db.session.add(self)
        db.session.commit()
