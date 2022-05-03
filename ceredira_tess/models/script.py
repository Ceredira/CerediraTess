from ceredira_tess.db import db
from ceredira_tess.models import relationships


class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2048), nullable=False, unique=True)
    description = db.Column(db.Text)
    agents = db.relationship("Agent", secondary=relationships.agents_scripts, back_populates='scripts')

    def __repr__(self):
        return f'{self.name}'
