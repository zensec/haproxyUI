from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class ClusterForm(Form):
    name = StringField('Name: ', validators=[DataRequired()])
