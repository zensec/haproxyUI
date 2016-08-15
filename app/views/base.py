from flask_classful import FlaskView
from app.decorators import login_required, global_variables


class BaseView(FlaskView):
    decorators = [login_required, global_variables]
