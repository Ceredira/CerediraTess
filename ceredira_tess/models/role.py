from flask_security import RoleMixin

from ceredira_tess.db import db
from ceredira_tess.models import relationships


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(255))
    agents = db.relationship("Agent", secondary=relationships.roles_agents, back_populates='roles')
    users = db.relationship("User", secondary=relationships.roles_users, back_populates='roles')

    def __repr__(self):
        return f'{self.name}'

    def __init__(self, name):
        self.name = name
