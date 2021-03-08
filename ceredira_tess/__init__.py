__author__ = 'unixshaman'

import base64
import os

from flask import Flask, url_for
from flask_admin import helpers
from flask_admin.menu import MenuLink
from flask_babelex import Babel
from flask_security import SQLAlchemyUserDatastore, Security, hash_password

# It's not strictly necessary to import these, but I do it here for PyInstaller
# (see https://github.com/pyinstaller/pyinstaller/issues/649)
import cffi
import configparser
import passlib.handlers
import passlib.handlers.sha2_crypt
import passlib.handlers.bcrypt
import passlib.handlers.des_crypt
import passlib.handlers.pbkdf2
import passlib.handlers.misc
from flask_security.utils import set_request_attr

import config
from ceredira_tess.db import db
from ceredira_tess.forms import MyAdminIndexView, LoginForm, UserModelView, RoleModelView, \
    OperationSystemTypeModelView, AgentModelView, ScriptModelView
from ceredira_tess.models.agent import Agent
from ceredira_tess.models.operation_system_type import OperationSystemType
from ceredira_tess.models.role import Role
from ceredira_tess.models.script import Script
from ceredira_tess.models.user import User
from ceredira_tess.views import *
from ceredira_tess.views.static import *
from ceredira_tess.views.www import *


def create_app():

    app = Flask(__name__,
                static_url_path='/static',
                static_folder='static',
                template_folder='templates',
                instance_relative_config=True
                )
    app.config.from_object(config.Config)

    db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)

    security = Security(app, user_datastore, login_form=LoginForm)
    babel = Babel(app, default_locale='ru')

    with app.test_request_context():
        if not os.path.isfile(app.config.get('SQLALCHEMY_DATABASE_URI').replace('sqlite:///', '')):
            db.create_all()

            admin_role = Role('admin')
            db.session.add(admin_role)
            db.session.commit()

            linux = OperationSystemType('Linux')
            windows = OperationSystemType('Windows')
            db.session.add_all([linux, windows])
            db.session.commit()

            ct_agent = Agent('CerediraTess', windows)
            ct_agent.add_role(admin_role)
            db.session.add(ct_agent)
            db.session.commit()

            user_datastore.create_user(email='admin@admin.ru', password=hash_password("admin"), roles=[admin_role],
                                       username='admin')
            db.session.commit()

    with app.app_context():
        import flask_admin as admin
        # Create admin
        admin = admin.Admin(app, 'CerediraTess', template_mode='bootstrap4', index_view=MyAdminIndexView(),
                            base_template='my_master.html', static_url_path='../static')

        admin.add_link(MenuLink(name='Выполнение запросов', category='', url='/CerediraTess.html'))
        admin.add_link(MenuLink(name='Блокировка агентов', category='', url='/AgentLocker.html'))

        admin.add_view(UserModelView(User, db.session, endpoint='User', name='Пользователи'))
        admin.add_view(RoleModelView(Role, db.session, endpoint='Role', name='Роли'))
        admin.add_view(OperationSystemTypeModelView(OperationSystemType, db.session, endpoint='OperationSystemType',
                                                    name='Типы ОС'))
        admin.add_view(AgentModelView(Agent, db.session, endpoint='Agent', name='Агенты'))
        admin.add_view(ScriptModelView(Script, db.session, endpoint='Script', name='Скрипты'))

        from ceredira_tess.commons import app as app2
        app.register_blueprint(app2)

    @babel.localeselector
    def get_locale():
        # Put your logic here. Application can store locale in
        # user profile, cookie, session, etc.
        return 'ru'

    @app.context_processor
    def inject_url():
        return dict(
            admin_view=admin.index_view,
            get_url=url_for,
            role=Role
        )

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=helpers,
            get_url=url_for,
            role=Role
        )

    return app
