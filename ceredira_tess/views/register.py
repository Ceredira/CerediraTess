import flask_login
from flask import url_for, request, render_template
from flask_admin import helpers
from werkzeug.utils import redirect

from ceredira_tess.commons import app
from ceredira_tess.db import db
from ceredira_tess.forms import RegistrationForm
from ceredira_tess.models.user import User


@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if helpers.validate_form_on_submit(form):
        # user = User()
        #
        # form.populate_obj(user)
        # # we hash the users password to avoid saving it as plaintext in the db,
        # # remove to use plain text:
        # user.set_password('1qaz@WSX')
        #
        # db.session.add(user)
        # db.session.commit()
        #
        # flask_login.login_user(user)
        return redirect(url_for('.ceredira_tess'))

    return render_template('register.html', form=form)
