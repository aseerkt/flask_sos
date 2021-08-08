from flask import Blueprint, render_template, request, flash, url_for
from flask_login import current_user, login_required
from . import db
from .models import Contact
from .utils import is_email

views = Blueprint("views", __name__)


@views.route('/')
def home():
    contacts = None
    if current_user.is_authenticated:
        contacts = Contact.query.filter_by(user_id=current_user.id).all()
    sos_btn_disabled = not current_user.is_authenticated or len(contacts) < 1
    print(sos_btn_disabled)
    return render_template('home.html', contacts=contacts, sos_btn_disabled=sos_btn_disabled)


@views.route('/contacts', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def contacts():
    contacts = None
    if current_user.is_authenticated:
        contacts = Contact.query.filter_by(user_id=current_user.id).all()

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
        if len(mobile_number) < 10:
            error = True
            flash('invalid number', category='danger')

        if not error:
            contact = Contact(full_name=full_name, email=email,
                              mobile_number=int(mobile_number), user_id=current_user.id)
            db.session.add(contact)
            db.session.commit()
            contacts.append(contact)

    return render_template('contacts.html', contacts=contacts)
