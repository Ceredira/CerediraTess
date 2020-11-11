import flask_login
from flask import url_for
from werkzeug.utils import redirect

from ceredira_tess.commons import app


@app.route('/logout.html')
def logout():
    flask_login.logout_user()
    return redirect(url_for('.ceredira_tess'))
