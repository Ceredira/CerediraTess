from flask_login import login_required

from ceredira_tess.commons import app


@app.route('/static/<path:path>')
@login_required
def send_static(path):
    return app.send_static_file(path)
