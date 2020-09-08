import flask_admin as admin
import flask_login as login
from flask import url_for, request
from flask_admin import helpers, expose
from flask_admin.contrib import sqla
from werkzeug.utils import redirect
from wtforms import form, fields, validators

from cerediratess.db import db
from cerediratess.models.Role import Role
from cerediratess.models.User import User


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
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Нет аккаунта? <a href="' + url_for('.register_view') + '">Нажмите тут для регистрации.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.set_password('1qaz@WSX')

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('app.ceredira_tess'))
        link = '<p>Нет аккаунта? <a href="' + url_for('.register_view') + '">Нажмите тут для регистрации.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('app.ceredira_tess'))
