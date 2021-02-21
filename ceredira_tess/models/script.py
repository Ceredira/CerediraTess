from ceredira_tess.db import db


class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scriptname = db.Column(db.String(2048), nullable=False, unique=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'{self.scriptname}'
