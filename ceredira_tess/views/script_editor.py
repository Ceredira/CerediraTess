import json
import os

from flask import render_template, request
from flask_security.decorators import auth_required

from ceredira_tess.commons import app
from ceredira_tess.models.role import Role
from config import BASEDIR


@app.route('/ScriptEditor.html', methods=['GET', 'POST'], endpoint='ScriptEditor')
@auth_required('session', 'token')
def agent_locker():
    return render_template('ScriptEditor.html', role=Role)


@app.route('/getScript/<path:script_name>', methods=['GET', 'POST'], endpoint='getScript')
@auth_required('session', 'token', 'basic')
def get_script(script_name):
    def get_script_body(root_path, script):
        try:
            with open(os.path.join(root_path, 'scripts', script), encoding='utf-8') as script_file:
                result = script_file.read()

        except EnvironmentError:
            result = {'exception': 'Файл скрипта не обнаружен.'}
        except Exception as ex:
            result = {'exception': f"Ошибка открытия файла скрипта: {ex}"}

        return result

    script_name = script_name.replace('/', '\\')

    res_info = {script_name: get_script_body(BASEDIR, script_name)}

    return json.dumps(res_info, indent=4, ensure_ascii=False), 200


@app.route('/saveScript/<path:script_name>', methods=['POST'], endpoint='saveScript')
@auth_required('session', 'token', 'basic')
def get_script(script_name):
    script_name = script_name.replace('/', '\\')
    try:
        with open(r'{}'.format(os.path.join(BASEDIR, 'scripts', script_name)), "w", encoding="UTF-8") as file:
            file.write(request.data.decode("utf-8").replace('\r', ''))
    except Exception as err:
        return str(err), 500

    return "Ok", 200
