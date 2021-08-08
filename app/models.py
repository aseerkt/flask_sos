from flask_login import UserMixin
from datetime import datetime
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), index=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False,
                        default='SOS! I am in danger, please help me!!')
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, default=datetime.now())

    contacts = db.relationship('Contact', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.full_name


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    mobile_number = db.Column(db.BigInteger, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)

    def __repr__(self):
        return '<Contact %r>' % self.full_name
