import json

import flask_login as login
from flask import request
from flask_login import login_required

from ceredira_tess.commons import app, agents_locker


@app.route('/agentsUnlock', methods=['POST'])
@login_required
def agents_unlock():
    user = login.current_user

    js_receive = request.get_json()
    hostnames = js_receive.get('hostnames', [])
    lock_cause = js_receive.get('lockCause', None)

    if not lock_cause:
        return f'LockCause must be specified in request body.', 400

    res = agents_locker.agents_unlock(user, hostnames, lock_cause)

    return json.dumps(res, indent=4, ensure_ascii=False), 200
