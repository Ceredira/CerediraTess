from cerediratess import app


@app.route('/static/<path:path>')
@login_required
def send_static(path):
    return app.send_static_file(path)