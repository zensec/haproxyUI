from flask_wtf import Form
from app.models.cluster import Cluster
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class DomainForm(Form):
    cluster_id = SelectField('Cluster: ', coerce=int, validators=[DataRequired()])
    name = StringField('Name: ', validators=[DataRequired()])

    def generate_cluster_id_options(self):
        clusters = Cluster.query.filter_by(audit_is_deleted=False, is_active=True).all()
        self.cluster_id.choices = [(c.id, c.name) for c in clusters]
