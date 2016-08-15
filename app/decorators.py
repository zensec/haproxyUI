from flask import g, session, redirect, url_for
from app.models.user import User
from app import app
from functools import wraps
from datetime import datetime, timedelta


def global_variables(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.release = {
            'version': app.config['RELEASE_VERSION'],
            'date': app.config['RELEASE_DATE'],
        }
        try:
            from app.globals import setup_custom_globals
            c = setup_custom_globals()
            if not c[0]:
                raise Exception('Error {0} raised, Cannot continue'.format(c[1]))
        except ImportError:
            raise Exception('Missing custom globals file, Application configuration error')
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            app.logger.debug('No user session found, Redirecting to login')
            return redirect(url_for('Login:index'))
        user_id = session['user_id']
        app.logger.debug('Retrieved {0} from session'.format(user_id))
        user = User.query.get(user_id)
        app.logger.debug('User determined to be {0}'.format(user.name))
        if user.last_seen < datetime.utcnow() - timedelta(minutes=15):
            app.logger.debug('User session older than 15 minutes ago, Redirecting to login')
            del session['user_id']
            return redirect(url_for('Login:index'))
        if not user.is_active:
            app.logger.debug('User not active, Redirecting ot login')
            del session['user_id']
            return redirect(url_for('Login:index'))
        app.logger.debug('User authenticated successfully, Allowing through')

        # Update our last seen & add to our globals
        g.user = user
        g.user.last_seen = datetime.utcnow()
        g.user.update()

        return f(*args, **kwargs)
    return decorated_function

