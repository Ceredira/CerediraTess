import flask_login as login
from flask import request
from flask_security.decorators import auth_required

from ceredira_tess.commons import app
from config import BASEDIR


@app.route('/executeScript/<path:script_name>', methods=['POST'], endpoint='executeScript')
@auth_required('session', 'token', 'basic')
def execute_script(script_name):
    js_receive = request.get_json()
    args = js_receive.get('args', [])
    hostname = js_receive.get('hostname', 'CerediraTess')
    username = js_receive.get('username', None)
    password = js_receive.get('password', None)
    elevated = js_receive.get('elevated', None)
    encoding = js_receive.get('encoding', 'utf-8')
    timeout = js_receive.get('timeout', 60)

    script_name = script_name.replace('/', '\\')

    user = login.current_user
    agents = [agent for x in user.roles for agent in x.agents]
    agent = next((x for x in agents if x.hostname == hostname), None)

    # Проверка существования агента в списке доступных агентов
    if not agent:
        return f'Host {hostname} not available for execution scripts', 404

    # if user.username not in agent.users:
    #     return f'User {user.username} not allowed for execution scripts on host {hostname}', 405

    # Проверка допустимости выполнения указанного скрипта на выбранном агенте
    # if script_name not in agent.scripts:
    if not [script for script in agent.scripts if script.name == script_name]:
        return f'Script {script_name} not available for execution on host {hostname}', 403

    res = agent.execute_script_with_timeout(BASEDIR, script_name,
                                            {'username': username, 'password': password, 'elevated': elevated},
                                            args, encoding, timeout)
    return res, 200
