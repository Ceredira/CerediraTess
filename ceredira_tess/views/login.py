import flask_login
from flask import url_for, request, render_template
from flask_admin import helpers
from werkzeug.utils import redirect

from ceredira_tess.commons import app
from ceredira_tess.forms import LoginForm


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if helpers.validate_form_on_submit(form):
        user = form.get_user()
        if user:
            if user.check_password(form.password.data):
                flask_login.login_user(user)
        else:
            return redirect(url_for('.ceredira_tess'))

    if flask_login.current_user.is_authenticated:
        # if referrer is not None and 'login.html' not in referrer:
        url = request.args.get('url')

        if url is not None and 'login.html' not in url:
            return redirect(url)
        else:
            return redirect(url_for('.ceredira_tess'))

    link = f'<p>Нет аккаунта? <a href="{url_for(".register")}">Нажмите тут для регистрации.</a></p>'

    return render_template('login.html', form=form, link=link)
