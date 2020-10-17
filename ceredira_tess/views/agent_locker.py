import flask_login as login
from flask import url_for, render_template, request
from flask_admin import helpers

from ceredira_tess.commons import app
from ceredira_tess.forms import LoginForm
from ceredira_tess.models.role import Role


@app.route('/AgentLocker.html', methods=('GET', 'POST'))
def agent_locker():
    form = LoginForm(request.form)
    link = '<p>Нет аккаунта? <a href="' + url_for('admin.register_view') + '">Нажмите тут для регистрации.</a></p>'
    if helpers.validate_form_on_submit(form):
        user = form.get_user()
        login.login_user(user)
    return render_template('AgentLocker.html', role=Role, form=form, link=link)
