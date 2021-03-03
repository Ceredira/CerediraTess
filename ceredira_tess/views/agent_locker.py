from flask import render_template
from flask_security.decorators import auth_required

from ceredira_tess.commons import app
from ceredira_tess.models.role import Role


@app.route('/AgentLocker.html', methods=['GET', 'POST'], endpoint='AgentLocker')
@auth_required('session', 'token')
def agent_locker():
    return render_template('AgentLocker.html', role=Role)
