import uuid

import flask_admin as admin
from flask import url_for, request, flash, abort, current_app, redirect
from flask_admin import expose
from flask_admin.babel import gettext
from flask_admin.contrib import sqla
from flask_admin.form import FormOpts
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_admin.model.template import LinkRowAction
from flask_security.confirmable import requires_confirmation
from flask_security.forms import Form, NextFormMixin, password_required, _security
from flask_security.utils import config_value, url_for_security, get_message, hash_password, find_user, current_user,\
    logout_user
from markupsafe import Markup
from wtforms import form, fields, validators, StringField, PasswordField, BooleanField, SubmitField

from ceredira_tess.db import db
from ceredira_tess.models.role import Role
from ceredira_tess.models.user import User


class RegistrationForm(form.Form):
    username = fields.StringField(validators=[validators.input_required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.input_required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(username=self.username.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


class BaseModelView(sqla.ModelView):
    column_extra_row_actions = [
        LinkRowAction(
            icon_class='fa fa-copy glyphicon glyphicon-duplicate',
            # Calls the .../duplicate?id={row_id} view
            # with the row_id from the Jinja template
            url='duplicate?id={row_id}',
            title="Дублировать запись"
        ),
    ]

    column_hide_backrefs = False
    can_view_details = True
    edit_modal = True
    create_modal = True
    details_modal = True
    
    def on_model_delete(self, model):
        if type(model) is User and model.username == 'admin':
            raise Exception('Нельзя удалить пользователя admin.')
        if type(model) is Role and model.name == 'admin':
            raise Exception('Нельзя удалить роль admin.')

    @expose('/duplicate/', methods=('GET', 'POST'))
    def duplicate_view(self):
        """
            Duplicate model view
        """
        return_url = get_redirect_target() or self.get_url('.index_view')

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)

        form = self.edit_form(obj=model)
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_create_rules, form=form)

        if self.validate_form(form):
            # in versions 1.1.0 and before, this returns a boolean
            # in later versions, this is the model itself
            model = self.create_model(form)

            if model:
                flash(gettext('Record was successfully created.'), 'success')
                if '_add_another' in request.form:
                    return redirect(request.url)
                elif '_continue_editing' in request.form:
                    # if we have a valid model, try to go to the edit view
                    if model is not True:
                        url = self.get_url('.edit_view', id=self.get_pk_value(model), url=return_url)
                    else:
                        url = return_url
                    return redirect(url)
                else:
                    # save button
                    return redirect(self.get_save_return_url(model, is_created=True))

        if request.method == 'GET' or form.errors:
            self.on_form_prefill(form, id)

        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        if self.edit_modal and request.args.get('modal'):
            template = self.edit_modal_template
        else:
            template = self.edit_template

        return self.render(template,
                           model=model,
                           form=form,
                           form_opts=form_opts,
                           return_url=return_url)

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin')
                )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


class AgentModelView(BaseModelView):
    column_labels = dict(
        hostname='Адрес агента (FQDN)',
        description='Описание',
        lock_cause='Причина блокировки',
        lock_user='Кем заблокировано',
        operationsystemtype='Тип ОС',
        scripts='Скрипты',
        roles='Роли'
    )

    column_list = ('hostname', 'operationsystemtype', 'description', 'lock_user', 'lock_cause', 'scripts', 'roles')
    column_details_list = ('hostname', 'operationsystemtype', 'description', 'lock_user', 'lock_cause', 'scripts', 'roles')
    form_columns = ('hostname', 'operationsystemtype', 'description', 'roles', 'scripts', 'lock_user', 'lock_cause')

class OperationSystemTypeModelView(BaseModelView):
    column_labels = dict(
        osname='Имя ОС'
    )

    column_list = ('osname',)
    column_details_list = ('osname',)
    form_columns = ('osname',)


class RoleModelView(BaseModelView):
    column_labels = dict(
        name='Название роли',
        description='Описание',
        agents='Агенты',
        users='Пользователи'
    )

    column_list = ('name', 'description', 'agents', 'users')
    column_details_list = ('name', 'description', 'agents', 'users')
    form_columns = ('name', 'description', 'users', 'agents')

class ScriptModelView(BaseModelView):
    column_labels = dict(
        name='Имя скрипта',
        description='Описание',
        agents='Агенты'
    )

    column_descriptions = dict(
        name='Путь к исполняемому файлу (*.bat, *.exe, *.vbs) от каталога scripts.\nНапример:'
             'test_script.bat - скрипт в корне каталога,\n'
             'common\\test_name_1.bat - скрипт в каталоге common,\n'
             'project_name\\tool.exe - путь к утилите tool.exe в каталоге с именем проекта',
        description='Произвольное текстовое описание скрипта, отличается то того, что в файлах скриптов с '
                    'REM DESCRIPTION'
    )

    column_list = ('name', 'description', 'agents')
    column_details_list = ('name', 'description', 'agents')
    form_columns = ('name', 'description', 'agents')

class UserModelView(BaseModelView):
    column_labels = dict(
        name='Имя пользователя',
        username='Логин пользователя',
        email='Почта',
        created_on='Дата создания',
        updated_on='Последнее обновление',
        active='Активный',
        roles='Роли',
        last_login_at='Последний вход',
        current_login_at='Текущий вход',
        last_login_ip='Последний адрес входа',
        current_login_ip='Текущий адрес входа',
        login_count='Количество входов',
        confirmed_at='Дата подтверждения УЗ'
    )

    column_list = ('username', 'active', 'email', 'name', 'created_on', 'updated_on', 'roles')
    column_details_list = ('username', 'active', 'email', 'name', 'created_on', 'updated_on', 'roles',
                           'last_login_at', 'current_login_at', 'last_login_ip', 'current_login_ip',
                           'login_count', 'confirmed_at')
    form_columns = ('username', 'active', 'password2', 'confirm', 'email', 'name', 'roles')

    def on_model_change(self, form, model, is_created):
        if model.fs_uniquifier is None:
            model.fs_uniquifier = uuid.uuid4().hex

    def get_create_form(self):
        self.form_extra_fields = {
            'password2': PasswordField('Пароль', [validators.input_required('Необходимо указать пароль'),
                                                  validators.EqualTo('confirm', message='Пароли не совпадают')]),
            'confirm': PasswordField('Подтверждение пароля', [validators.input_required('Необходимо повторно указать пароль')])
        }
        return self.get_form()

    def get_edit_form(self):
        self.form_extra_fields = {
            'password2': PasswordField('Пароль', [validators.EqualTo('confirm', message='Пароли не совпадают')]),
            'confirm': PasswordField('Подтверждение пароля')
        }
        return self.get_form()


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        self._template_args['role'] = Role
        if not current_user.is_authenticated:
            return redirect(url_for('security.login', url=request.url_rule))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_page(self):
        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_page(self):
        logout_user()
        return redirect(url_for('.index'))

    @expose('/reset/')
    def reset_page(self):
        return redirect(url_for('.index'))


class LoginForm(Form, NextFormMixin):
    """Customized login form"""

    username = StringField(validators=[validators.input_required('Пользователь незарегистрирован')])
    password = PasswordField(validators=[password_required])
    remember = BooleanField()
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = request.args.get("next", "")
        self.remember.default = config_value("DEFAULT_REMEMBER_ME")
        if (
            current_app.extensions["security"].recoverable
            and not self.password.description
        ):
            html = Markup(
                '<a href="{url}">{message}</a>'.format(
                    url=url_for_security("forgot_password"),
                    message=get_message("FORGOT_PASSWORD")[0],
                )
            )
            self.password.description = html
        self.requires_confirmation = False

    def validate(self):
        if not super().validate():
            return False

        self.user = find_user(self.username.data)

        if self.user is None:
            self.username.errors.append(get_message("USER_DOES_NOT_EXIST")[0])
            # Reduce timing variation between existing and non-existing users
            hash_password(self.password.data)
            return False
        if not self.user.password:
            self.password.errors.append(get_message("PASSWORD_NOT_SET")[0])
            # Reduce timing variation between existing and non-existing users
            hash_password(self.password.data)
            return False
        self.password.data = _security._password_util.normalize(self.password.data)
        if not self.user.verify_and_update_password(self.password.data):
            self.password.errors.append(get_message("INVALID_PASSWORD")[0])
            return False
        self.requires_confirmation = requires_confirmation(self.user)
        if self.requires_confirmation:
            self.username.errors.append(get_message("CONFIRMATION_REQUIRED")[0])
            return False
        if not self.user.is_active:
            self.username.errors.append(get_message("DISABLED_ACCOUNT")[0])
            return False
        return True
