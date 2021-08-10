from os import getenv
from flask import Blueprint, render_template, request, flash, url_for, redirect, abort
from flask_login import current_user, login_required
from . import db
from .models import Contact, User
from .utils import is_email, get_location_url
import requests
import json

views = Blueprint("views", __name__)


@views.route('/')
def home():
    contacts = None
    if current_user.is_authenticated:
        contacts = Contact.query.filter_by(user_id=current_user.id).all()
    sos_btn_disabled = not current_user.is_authenticated or len(contacts) < 1
    print(sos_btn_disabled)
    return render_template('home.html', contacts=contacts, sos_btn_disabled=sos_btn_disabled)


@views.route('/contacts', methods=['POST', 'PUT', 'DELETE'])
@login_required
def contacts():

    if (request.method == 'POST'):
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        mobile_number = request.form.get('mobile_number')

        error = False

        if len(full_name) < 4:
            error = True
            flash('Full name is too short', category='danger')
        if not is_email(email):
            error = True
            flash('Email is invalid', category='danger')
        if len(mobile_number) != 10:
            error = True
            flash('Invalid phone number', category='danger')

        if not error:
            contact = Contact(full_name=full_name, email=email,
                              mobile_number=int(mobile_number), user_id=current_user.id)
            db.session.add(contact)
            db.session.commit()

        return redirect(url_for('views.home'))


@views.route('/message', methods=['POST'])
@login_required
def edit_message():
    if request.method == 'POST':
        message = request.form.get('message')

        if (current_user.message != message):
            user = User.query.filter_by(id=current_user.id).first()
            user.message = message
            db.session.commit()

        return redirect(url_for('views.home'))


@views.route('/send-message', methods=['POST'])
@login_required
def send_bulk_mail():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    def get_numbers(contact):
        return f"+91{contact.mobile_number}"

    contacts = Contact.query.filter_by(user_id=current_user.id).all()

    data = {
        "to": list(map(get_numbers, contacts)),
        "body": current_user.message + ' ' + get_location_url(latitude, longitude)
    }
    print(data)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Basic {getenv('BULK_SMS_BASIC_AUTH')}"
    }

    res = requests.post('https://api.bulksms.com/v1/messages',
                        data=json.dumps(data), headers=headers)

    print('Returend data')
    print(res.json())
    print('Returend status code')
    print(res.status_code)

    if (res.status_code != 201):
        return abort(res.status_code, description=res.json())

    return res.json()
