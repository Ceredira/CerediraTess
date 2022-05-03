from datetime import datetime
from flask_security import UserMixin, hash_password
from sqlalchemy.ext.hybrid import hybrid_property

from ceredira_tess.db import db
from ceredira_tess.models import relationships


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(255), unique=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    password = db.Column(db.String(150), nullable=False)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    active = db.Column(db.Boolean())
    # roles = db.relationship("Role", secondary=relationships.roles_users, backref=db.backref('users', lazy='dynamic'))
    roles = db.relationship("Role", secondary=relationships.roles_users, back_populates='users')

    def __repr__(self):
        return f'{self.username}'

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    @hybrid_property
    def password2(self):
        """Return the hashed user password."""
        return self.password

    @password2.setter
    def password2(self, new_password2):
        """Hash and save the user's new password."""
        self.password = hash_password(new_password2)
