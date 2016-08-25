from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class UpstreamForm(Form):
    ip_address = StringField('Address: ', validators=[DataRequired()])
    port = IntegerField('Port: ', validators=[DataRequired()])
