import flask_admin as admin
import flask_login as login
from flask import url_for, request
from flask_admin import expose
from flask_admin.contrib import sqla
from werkzeug.utils import redirect
from wtforms import form, fields, validators

from ceredira_tess.db import db
from ceredira_tess.models.role import Role
from ceredira_tess.models.user import User


class LoginForm(form.Form):
    username = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not user.check_password(user.password):
            # to compare plain text passwords use
            # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(username=self.username.data).first()


class RegistrationForm(form.Form):
    username = fields.StringField(validators=[validators.required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(username=self.username.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


# Create customized model view class
class MyModelView(sqla.ModelView):
    column_labels = dict(
        osname='Имя ОС',
        rolename='Название роли',
        hostname='Адрес агента',
        description='Описание',
        operationsystemtype='Тип ОС',
        scripts='Скрипты',
        agents='Агенты',
        scriptname='Имя скрипта',
        username='Имя пользователя',
        salt='Соль',
        key='Ключ',
        roles='Роли',
        lock_user='Кем заблокировано',
        lock_cause='Причина блокировки'
    )

    def is_accessible(self):
        if login.current_user.is_authenticated:
            if Role.query.filter_by(rolename='admin').first() in login.current_user.roles:
                return True

        return False


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        self._template_args['role'] = Role
        if not login.current_user.is_authenticated:
            return redirect(url_for('app.login', url=request.url_rule))
        return super(MyAdminIndexView, self).index()
