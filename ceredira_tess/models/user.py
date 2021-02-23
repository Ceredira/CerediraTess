from datetime import datetime

from flask_security.utils import verify_password, hash_password

from ceredira_tess.db import db
from ceredira_tess.models import relationships


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String, unique=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    password = db.Column(db.String(64))
    active = db.Column(db.Boolean())
    roles = db.relationship("Role", secondary=relationships.roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'{self.username}'

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def add_role(self, role):
        self.roles.append(role)

    def add_roles(self, roles):
        self.roles.extend(roles)

    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        return verify_password(password, self.password)

    # Flask - Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Flask-Security
    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    # Required for administrative interface
    def __unicode__(self):
        return self.username
