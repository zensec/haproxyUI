from flask_classful import FlaskView
from flask import redirect, url_for
from app.decorators import login_required, global_variables
from app import app


class BaseView(FlaskView):
    trailing_slash = False
    decorators = [login_required, global_variables]


@app.route('/')
def index():
    return redirect(url_for('Dashboard:index'))
