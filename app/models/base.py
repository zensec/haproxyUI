from datetime import datetime

from flask import g

from app import db, app
from app.helpers import parse_to_dict


class Audit(db.Model):
    __abstract__ = True

    audit_created_by = db.Column(db.Integer)
    audit_updated_by = db.Column(db.Integer)
    audit_deleted_by = db.Column(db.Integer)

    audit_created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    audit_updated_on = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    audit_deleted_on = db.Column(db.DateTime)

    audit_is_deleted = db.Column(db.Boolean, default=False)

    def create(self):
        try:
            self.audit_created_by = g.user.id
        except RuntimeError:
            self.audit_created_by = get_maintenance_user_id()
        self.audit_is_deleted = False
        self.audit_created_on = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self):
        try:
            self.audit_updated_by = g.user.id
        except RuntimeError:
            self.audit_updated_by = get_maintenance_user_id()
        self.audit_updated_on = datetime.utcnow()
        db.session.commit()

    def delete(self):
        try:
            self.audit_deleted_by = g.user.id
        except RuntimeError:
            self.audit_deleted_by = get_maintenance_user_id()
        self.audit_deleted_on = datetime.utcnow()
        self.audit_is_deleted = True
        db.session.commit()


class Configuration(db.Model):
    __tablename__ = 'configuration'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100))
    value = db.Column(db.Boolean, default=False)


def get_maintenance_user_id():
    from .user import User
    user = User.query.filter_by(name='Maintenance').first()
    if not user:
        user = User(name='Maintenance', username='Maintenance', is_active=False)
        db.sessionn.add(user)
        db.session.commit()
    return user.id
