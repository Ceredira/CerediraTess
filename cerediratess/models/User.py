import hashlib
import os

from cerediratess.db import db
from cerediratess.models import relationships


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    salt = db.Column(db.String(64))
    key = db.Column(db.String(64))
    roles = db.relationship("Role", secondary=relationships.user_roles)

    def __repr__(self):
        return f'{self.username} {self.roles}'

    def set_password(self, password):
        salt_binary = os.urandom(32)  # A new salt for this user
        self.salt = salt_binary.hex()
        self.key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_binary, 10000).hex()

    def check_password(self, password):
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(self.salt), 10000).hex()
        if self.key == new_key:
            return True
        else:
            return False

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

    # Required for administrative interface
    def __unicode__(self):
        return self.username
