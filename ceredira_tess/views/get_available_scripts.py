import json
import os
import re

import flask_login as login
from flask_login import login_required

from ceredira_tess.commons import app
from config import BASEDIR


@app.route('/getAvailableScripts', methods=['POST'])
@login_required
def get_available_scripts():
    def parse_script_metadata(root_path, script):
        try:
            with open(os.path.join(root_path, 'scripts', script), encoding='utf-8') as script_file:
                script_content = script_file.read()

            try:
                script_description = re.findall(r'rem script description: (.*)', script_content)
                script_args_desc = re.findall(r'rem arg description: (.*)', script_content)
                script_args_example = re.findall(r'rem arg example: (.*)', script_content)
                script_execution_check = re.findall(r'rem script checking: (.*)', script_content)
                script_encoding = re.findall(r'rem script encoding: (.*)', script_content)
                script_timeout = re.findall(r'rem script timeout: (.*)', script_content)

                result = {
                    'arguments': script_args_example,
                    'argumentsDescription': script_args_desc,
                    'description': '\n'.join(script_description),
                    'executionCheck': [[y.strip() for y in x.split('||')] for x in script_execution_check],
                    'timeout': script_timeout if script_timeout else 60,
                    'recommendedEncoding': ''.join(script_encoding) if script_encoding else None
                }
            except Exception as ex:
                result = {'exception': f"Ошибка обработки файла скрипта: {ex}"}
        except EnvironmentError:
            result = {'exception': 'Файл скрипта не обнаружен.'}
        except Exception as ex:
            result = {'exception': f"Ошибка открытия файла скрипта: {ex}"}

        return result

    user = login.current_user
    agents = [agent for x in user.roles for agent in x.agents]
    scripts = [script for x in agents for script in x.scripts]

    res_info = {}
    for script in scripts:
        script_metadata = parse_script_metadata(BASEDIR, script.name)
        script_metadata['agents'] = [x.hostname for x in agents] if 'exception' not in script_metadata else None
        res_info[script.name] = script_metadata

    return json.dumps(res_info, indent=4, ensure_ascii=False), 200
