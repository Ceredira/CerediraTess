from flask import render_template
from flask_security.decorators import auth_required

from ceredira_tess.commons import app
from ceredira_tess.models.role import Role


@app.route('/', methods=['GET', 'POST'], endpoint='main')
@app.route('/CerediraTess.html', methods=['GET', 'POST'], endpoint='CerediraTess')
@auth_required('session', 'token')
def ceredira_tess():
    return render_template('CerediraTess.html', role=Role)
