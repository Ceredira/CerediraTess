from flask_security.decorators import auth_required

from ceredira_tess.commons import app


@app.route('/static/<path:path>', endpoint='static')
@auth_required('session', 'token', 'basic')
def send_static(path):
    return app.send_static_file(path)
