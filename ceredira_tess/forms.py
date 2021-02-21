import flask_admin as admin
import flask_login as login
from flask import url_for, request, flash
from flask_admin import expose
from flask_admin.babel import gettext
from flask_admin.contrib import sqla
from flask_admin.form import FormOpts
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_admin.model.template import LinkRowAction
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

    column_extra_row_actions = [
        LinkRowAction(
            icon_class='fa fa-copy glyphicon glyphicon-duplicate',
            # Calls the .../duplicate?id={row_id} view
            # with the row_id from the Jinja template
            url='duplicate?id={row_id}',
            title="Duplicate Row"
        ),
    ]

    column_hide_backrefs = False
    # column_list = ('scripts', )
    # column_details_list = ('scripts', )
    can_view_details = True

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
