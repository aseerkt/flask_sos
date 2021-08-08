import re
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User
from .utils import is_email

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Email is not registered', category='danger')
        elif not check_password_hash(user.password, password):
            flash('Incorrect password', category='danger')
        else:
            login_user(user, remember=True)
            flash('Welcome {}'.format(user.full_name), category='success')
            return redirect(url_for('views.home'))

    return render_template('auth/login.html')


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if (request.method == 'POST'):
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_again = request.form.get('password_again')

        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            print('Email is already taken')
            flash('Email is already taken', category='danger')
        elif len(full_name) < 3:
            print('Full name is too short')
            flash('Full name is too short', category='danger')
        if not is_email(email):
            print('Invalid email address')
            flash('Invalid email address', category='danger')
        elif password != password_again:
            print('Passwords do not match')
            flash('Passwords do not match', category='danger')
        elif len(password) < 6:
            print('Password is too short')
            flash('Password is too short', category='danger')
        else:
            print('Made it here')
            new_user = User(full_name=full_name,
                            email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Welcome {}'.format(new_user.full_name), category='success')
            return redirect(url_for('views.home'))

    return render_template('auth/signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success', category='success')
    return redirect(url_for('views.home'))
