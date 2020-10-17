from ceredira_tess.db import db


class OperationSystemType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    osname = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'{self.osname}'
