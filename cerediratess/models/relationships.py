from cerediratess.db import db


user_roles = db.Table('user_roles', db.Model.metadata,
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                      )

role_agents = db.Table('role_agents', db.Model.metadata,
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                       db.Column('agent_id', db.Integer, db.ForeignKey('agent.id'))
                       )

agent_scripts = db.Table('agent_scripts', db.Model.metadata,
                         db.Column('agent_id', db.Integer, db.ForeignKey('agent.id')),
                         db.Column('script_id', db.Integer, db.ForeignKey('script.id'))
                         )
