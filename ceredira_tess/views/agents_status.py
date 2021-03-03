import json

import flask_login as login
from flask import request
from flask_security.decorators import auth_required

from ceredira_tess.commons import app, agents_locker
from ceredira_tess.models.agent import Agent


def encode_agent(o):
    if isinstance(o, Agent):
        return {'hostname': o.hostname,
                'lock_cause': o.lock_cause,
                'lock_user': o.lock_user.username if o.lock_user else None
                }
    else:
        type_name = o.__class__.__name__
        raise TypeError(f'Object of type "{type_name}" is not JSON serializable')


@app.route('/agentsStatus', methods=['POST'], endpoint='agentsStatus')
@auth_required('session', 'token', 'basic')
def agents_status():
    user = login.current_user

    js_receive = request.get_json()
    hostnames = js_receive.get('hostnames', [])

    res = agents_locker.agents_status(user, hostnames)

    return json.dumps(res, indent=4, ensure_ascii=False, default=encode_agent), 200
