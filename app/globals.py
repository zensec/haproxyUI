from app.models.base import Configuration
from flask import g, request


def setup_custom_globals():
    # Check maintenance mode
    maintenance_mode = Configuration.query.filter_by(key='enable_maintenance_mode').first()
    if maintenance_mode:
        if maintenance_mode.value:
            if 'post' in request.endpoint:
                message = 'The API is currently under routine maintenance, Please try your request later'
                return False, message, 503
    return True, ''
