from ceredira_tess.db import db


roles_users = db.Table('roles_users', db.Model.metadata,
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )

roles_agents = db.Table('roles_agents', db.Model.metadata,
                        db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                        db.Column('agent_id', db.Integer, db.ForeignKey('agent.id'))
                        )

agents_scripts = db.Table('agents_scripts', db.Model.metadata,
                          db.Column('agent_id', db.Integer, db.ForeignKey('agent.id')),
                          db.Column('script_id', db.Integer, db.ForeignKey('script.id'))
                          )
