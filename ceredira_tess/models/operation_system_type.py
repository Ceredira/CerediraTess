from ceredira_tess.db import db


class OperationSystemType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    osname = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return f'{self.osname}'

    def __init__(self, osname):
        self.osname = osname
