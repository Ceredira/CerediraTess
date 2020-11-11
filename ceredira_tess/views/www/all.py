import os

from flask import send_from_directory, abort, send_file

from ceredira_tess.commons import app
from config import BASEDIR


@app.route('/www/<path:path>')
def send_static_unauthorized(path):
    try:
        filename, file_extension = os.path.splitext(path)
        if file_extension == '.html' or file_extension == '.txt':
            return send_file(os.path.join(BASEDIR, 'www', path))
        else:
            return send_from_directory('../www/', filename=path, as_attachment=True)
    except FileNotFoundError:
        abort(404)
