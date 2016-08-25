from flask import render_template, request, flash, redirect, url_for, session, g
from app.models.user import User
from app.helpers import log
from flask_classful import FlaskView, route
from datetime import datetime
from app import app, db


class Auth(FlaskView):
    route_base = ''

    @route('/login')
    def index(self):
        return render_template('auth/login.html')

    @route('/login', methods=['POST'])
    def login(self):
        if 'user_id' in session:
            del session['user_id']

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Invalid username or password', 'error')
            return redirect(url_for('Auth:index'))

        if not user.validate_password(password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('Auth:index'))

        app.logger.debug('Storing user ID {0} into session'.format(user.id))
        session['user_id'] = user.id
        user.last_seen = datetime.utcnow()
        db.session.commit()
        g.user = user

        log()
        return redirect(url_for('Dashboard:index'))

    @route('/logout')
    def logout(self):
        if 'user_id' in session:
            del session['user_id']

        log()
        return redirect(url_for('Auth:index'))
