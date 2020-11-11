import flask_login as login
from flask import render_template, url_for, request
from werkzeug.utils import redirect

from ceredira_tess.commons import app
from ceredira_tess.models.role import Role


@app.route('/', methods=['GET', 'POST'])
@app.route('/CerediraTess.html', methods=['GET', 'POST'])
def ceredira_tess():
    if not login.current_user.is_authenticated:
        return redirect(url_for('.login', url=request.url_rule))
    else:
        return render_template('CerediraTess.html', role=Role)
