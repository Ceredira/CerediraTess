__author__ = 'unixshaman'
from flask import Flask, url_for
from flask_admin.menu import MenuLink
from flask_babelex import Babel

import config
from cerediratess.db import db
from cerediratess.forms import MyModelView, MyAdminIndexView
from cerediratess.models.Agent import Agent
from cerediratess.models.OperationSystemType import OperationSystemType
from cerediratess.models.Role import Role
from cerediratess.models.Script import Script
from cerediratess.models.User import User
from cerediratess.my_flask_login import init_login
from cerediratess.views import *


def create_app():

    app = Flask(__name__,
                static_url_path='/static',
                static_folder='static',
                template_folder='templates',
                instance_relative_config=True
                )
    app.config.from_object(config.Config)

    babel = Babel(app)
    db.init_app(app)

    init_login(app)

    with app.app_context():
        import flask_admin as admin
        # Create admin
        admin = admin.Admin(app, 'CerediraTess', template_mode='bootstrap3', index_view=MyAdminIndexView(),
                            base_template='my_master.html')

        admin.add_link(MenuLink(name='Выполнение запросов', category='', url='/CerediraTess.html'))
        admin.add_link(MenuLink(name='Блокировка агентов', category='', url='/AgentLocker.html'))

        admin.add_view(MyModelView(User, db.session, endpoint='User', name='Пользователи'))
        admin.add_view(MyModelView(Role, db.session, endpoint='Role', name='Роли'))
        admin.add_view(MyModelView(OperationSystemType, db.session, endpoint='OperationSystemType', name='Типы ОС'))
        admin.add_view(MyModelView(Agent, db.session, endpoint='Agent', name='Агенты'))
        admin.add_view(MyModelView(Script, db.session, endpoint='Script', name='Скрипты'))

        from cerediratess.commons import app as app2
        app.register_blueprint(app2)

    @app.context_processor
    def inject_url():
        return dict(
            admin_view=admin.index_view,
            get_url=url_for,
            role=Role
        )

    @babel.localeselector
    def get_locale():
        # Put your logic here. Application can store locale in
        # user profile, cookie, session, etc.
        return 'ru'

    return app
