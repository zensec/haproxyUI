from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class ServerForm(Form):
    name = StringField('Name: ', validators=[DataRequired()])
    ip_address = StringField('Address: ', validators=[DataRequired()])
