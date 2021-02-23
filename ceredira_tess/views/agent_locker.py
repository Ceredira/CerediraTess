import flask_login as login
from flask import render_template, url_for, request
from werkzeug.utils import redirect

from ceredira_tess.commons import app
from ceredira_tess.models.role import Role


@app.route('/AgentLocker.html', methods=['GET', 'POST'])
def agent_locker():
    if not login.current_user.is_authenticated:
        return redirect(url_for('security.login', url=request.url_rule))
    else:
        return render_template('AgentLocker.html', role=Role)
