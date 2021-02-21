from ceredira_tess.db import db
from ceredira_tess.models import relationships


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rolename = db.Column(db.String(64), nullable=False, unique=True)
    agents = db.relationship("Agent", secondary=relationships.role_agents, back_populates='roles')

    def __repr__(self):
        return f'{self.rolename}'

    def __init__(self, rolename):
        self.rolename = rolename
