from flask import render_template, request, flash, redirect, url_for, session
from app.models.user import User
from flask_classful import FlaskView
from datetime import datetime
from app import app, db


class Login(FlaskView):
    def index(self):
        return render_template('login/index.html')

    def post(self):
        if 'user_id' in session:
            del session['user_id']

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Invalid username1 or password', 'error')
            return redirect(url_for('Login:index'))

        if not user.validate_password(password):
            flash('Invalid username or password!', 'error')
            return redirect(url_for('Login:index'))

        app.logger.debug('Storing user ID {0} into session'.format(user.id))
        session['user_id'] = user.id
        user.last_seen = datetime.utcnow()
        db.session.commit()

        return redirect(url_for('Clusters:index'))
