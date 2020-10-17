import json

import flask_login as login
from flask import request
from flask_login import login_required

from ceredira_tess.commons import app, agents_locker


@app.route('/agentsLock', methods=['POST'])
@login_required
def agents_lock():
    user = login.current_user

    js_receive = request.get_json()
    hostnames = js_receive.get('hostnames', [])
    lock_cause = js_receive.get('lockCause', None)
    min_agents_count = js_receive.get('minAgentsCount', 1)
    max_agents_count = js_receive.get('maxAgentsCount', None)

    if not lock_cause:
        return f'LockCause must be specified in request body.', 400

    if not min_agents_count:
        return f'minAgentsCount must be specified in request body.', 400

    res = agents_locker.agents_lock(user, hostnames, lock_cause, min_agents_count, max_agents_count)

    return json.dumps(res, indent=4), 200
