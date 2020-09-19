import flask_login as login
from flask import render_template, request, url_for
from flask_admin import helpers

from cerediratess.commons import app
from cerediratess.forms import LoginForm
from cerediratess.models.role import Role


@app.route('/', methods=('GET', 'POST'))
@app.route('/CerediraTess.html', methods=('GET', 'POST'))
def ceredira_tess():
    form = LoginForm(request.form)
    link = '<p>Нет аккаунта? <a href="' + url_for('admin.register_view') + '">Нажмите тут для регистрации.</a></p>'
    if helpers.validate_form_on_submit(form):
        user = form.get_user()
        login.login_user(user)

    return render_template('CerediraTess.html', role=Role, form=form, link=link)
