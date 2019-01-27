from time import time
from flask import current_app, url_for
import jwt
from app import db, login
from hashlib import md5

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import MEDIUMINT, TINYINT, SMALLINT
import json

import base64
from datetime import datetime, timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.base_model import Base

association_table_unc = db.Table('association_unc',
    db.Column('uncertainty_id', db.Integer, db.ForeignKey('uncertainty.id')),
    db.Column('deparment_id', db.Integer, db.ForeignKey('department.id'))
)

association_table_dep = db.Table('association_dep',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('deparment_id', db.Integer, db.ForeignKey('department.id'))
)

class Usercategory(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)

    _default_fields = [
        "name"
    ]

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class Userstatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), index=True)
    _default_fields = [
        "status"
    ]
class User(Base, PaginatedAPIMixin, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    departments = db.relationship(
        "Department",
        secondary=association_table_dep,
        back_populates="users")
    category_id = db.Column(db.Integer, db.ForeignKey('usercategory.id'))
    category = db.relationship(
        "Usercategory", backref="users")
    status = db.Column(db.Integer, db.ForeignKey('userstatus.id'))
    _default_fields = [
        "username",
        "last_seen",
        "departments",
        "category_id",
        "about_me",
    ]
    _hidden_fields = [
        "password_hash",
        "token",
        "token_expiration",
    ]
    _readonly_fields = [
        "email_confirmed",
    ]

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    """
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])"""

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Documentcategory(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    _default_fields = [
        "name"
    ]

class Department(Base):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    location = db.Column(db.String(100), index=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship(
        "User",
        secondary=association_table_dep,
        back_populates="departments")
    uncertainties = db.relationship(
        "Uncertainty",
        secondary=association_table_unc,
        backref="departments")
    _default_fields = [
        "name",
        "designation",
        "location"
    ]


class Documentstatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), index=True)
    _default_fields = [
        "status"
    ]

class Document(Base):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(100), index=True, nullable=False)
    file = db.Column(db.String(500), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    uploader = db.relationship(
        "User",
        foreign_keys=[uploader_id],
        backref="documents_owned")
    status = db.Column(db.Integer, db.ForeignKey('documentstatus.id'))
    reviwer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewer = db.relationship(
        "User",
        foreign_keys=[reviwer_id],
        backref="documents_reviewed")
    version = db.Column(db.String(200), unique=True, nullable=False)
    uploaded = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.DateTime, default=None)
    last_reviewed = db.Column(db.DateTime, default=None)
    next_reviewed = db.Column(db.DateTime, default=None)
    category_id = db.Column(db.Integer, db.ForeignKey('documentcategory.id'))
    category = db.relationship(
        "Documentcategory", backref="documents")
    _default_fields = [
        "file",
        "uploaded",
        "owner_id",
        "reviwer_id",
        "version"
    ]

class Uncertainty(Base):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(200), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship(
        "User",
        foreign_keys=[owner_id],
        backref="uncertainties_owned")
    uploaded = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed = db.Column(db.DateTime, default=None)
    status = db.Column(db.Integer, db.ForeignKey('documentstatus.id'))
    reviwer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewer = db.relationship(
        "User",
        foreign_keys=[reviwer_id],
        backref="uncertainties_reviewed")
    version = db.Column(db.String(200), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('documentcategory.id'))
    category = db.relationship(
        "Documentcategory", backref="uncertainties")
    designation = db.Column(db.String(100), index=True)
    instrument = db.Column(db.String(100), index=True)
    subfield = db.Column(db.String(100))
    _default_fields = [
        "file",
        "uploaded",
        "owner_id",
        "reviwer_id",
        "version",
        "designation",
        "designation",
        "location"
    ]

class Message(Base):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    _default_fields = [
        "sender_id",
        "recipient_id",
        "body",
        "timestamp"
    ]

class Notification(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)
    _default_fields = [
        "name",
        "user_id",
        "timestamp",
        "payload_json"
    ]

    def get_data(self):
        return json.loads(str(self.payload_json))

class Taskcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)

class Task(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    addded_date = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    adder_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    adder = db.relationship(
        "User",
        foreign_keys=[adder_id],
        backref="tasks")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    complete = db.Column(db.Boolean, default=False)
    progress = db.Column(db.Integer)
    _default_fields = [
        "name",
        "description",
        "user_id",
        "complete"
    ]
workstation_instruments = db.Table('workstation_instruments',
    db.Column('instrument_id', db.Integer, db.ForeignKey('instrument.id')),
    db.Column('workstation_id', db.Integer, db.ForeignKey('workstation.id'))
)

"""
stores external database ids for quick access
"""
class Instrument(Base):
    id = db.Column(db.Integer, primary_key=True)
    mois_id = db.Column(db.Integer, nullable=False, unique=True, index=True)
    description = db.Column(db.String(200), nullable=False, index=True)
    data_fields_json = db.Column(db.Text)
    last_maintenance_date = db.Column(db.DateTime)
    last_maintenance_interval = db.Column(db.Integer)
    _default_fields = [
        "id",
        "mois_id",
        "description"
    ]
    def get_data(self):
        return json.loads(str(self.data_fields_json))

class Workstation(Base):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(200), nullable=True)
    designation = db.Column(db.String(200), nullable=True)
    scope = db.Column(db.String(200), nullable=True)
    instruments = db.relationship(
        "Instrument",
        secondary=workstation_instruments,
        backref="workstations")
    responsible_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    instruments = db.Column(db.Integer, db.ForeignKey('user.id'))

    version = db.Column(db.String(200), unique=True, nullable=False)

    uploaded = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.DateTime, default=None)
    last_reviewed = db.Column(db.DateTime, default=None)
    next_reviewed = db.Column(db.DateTime, default=None)

    _default_fields = [
        "file",
        "designation",
        "responsible_user_id",
        "version",
        "last_reviewed"
    ]
