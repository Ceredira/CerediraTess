#!/usr/bin/env python3
# coding=utf-8
"""
:author: unixshaman@gmail.com, gdjamalov@appline.com
Модуль для хранения статических функций обрабатывающих POST запросы к серверу
"""
import json
import logging

from CerediraTess import server

module_logger = logging.getLogger('CerediraTess.request_processor_post')


def post_response(body):
    """Выполнить указанный запрос HTTP.
    """
    js_receive = json.loads(body.decode('utf-8'))
    return 200, {}, bytes(f'hello world\n{json.dumps(js_receive, indent=4, ensure_ascii=False)}', 'utf8')


def execute_script(user, list_of_agents, script_name, body):
    js_receive = json.loads(body.decode('utf-8'))
    args = js_receive.get('args', [])
    hostname = js_receive.get('hostname', 'CerediraTess')
    username = js_receive.get('username', None)
    password = js_receive.get('password', None)
    encoding = js_receive.get('encoding', 'utf-8')
    timeout = js_receive.get('timeout', 60)

    agent = next((x for x in list_of_agents if x.hostname == hostname), None)
    # Проверка существования агента в списке доступных агентов
    if not agent:
        return 403, {}, bytes(f'Host {hostname} not available for execution scripts', 'utf-8')

    if user.username not in agent.users:
        return 405, {}, bytes(f'User {user.username} not allowed for execution scripts on host {hostname}', 'utf-8')

    # Проверка допустимости выполнения указанного скрипта на выбранном агенте
    if script_name not in agent.scripts:
        return 405, {}, bytes(f'Script {script_name} not available for execution on host {hostname}', 'utf-8')

    res = agent.execute_script_with_timeout(server.WEB_ROOT, script_name, hostname,
                                        {'username': username, 'password': password}, args, encoding, timeout)
    return 200, {}, bytes(res, 'utf8')


def agents_lock(agent_locker, user, body):
    js_receive = json.loads(body.decode('utf-8'))
    hostnames = js_receive.get('hostnames', [])
    lock_cause = js_receive.get('lockCause', None)
    min_agents_count = js_receive.get('minAgentsCount', 1)
    max_agents_count = js_receive.get('maxAgentsCount', None)

    if not lock_cause:
        return 403, {}, bytes(f'LockCause must be specified in request body.', 'utf-8')

    if not min_agents_count:
        return 403, {}, bytes(f'minAgentsCount must be specified in request body.', 'utf-8')

    res = agent_locker.agents_lock(user, hostnames, lock_cause, min_agents_count, max_agents_count)

    return 200, {}, bytes(json.dumps(res, indent=4), 'utf-8')


def agents_unlock(agent_locker, user, body):
    js_receive = json.loads(body.decode('utf-8'))
    hostnames = js_receive.get('hostnames', [])
    lock_cause = js_receive.get('lockCause', None)

    if not lock_cause:
        return 403, {}, bytes(f'LockCause must be specified in request body.', 'utf-8')

    res = agent_locker.agents_unlock(user, hostnames, lock_cause)

    return 200, {}, bytes(json.dumps(res, indent=4, ensure_ascii=True), 'utf-8')


def agents_status(agent_locker, user, body):
    js_receive = json.loads(body.decode('utf-8'))
    hostnames = js_receive.get('hostnames', [])

    res = agent_locker.agents_status(user, hostnames)

    return 200, {}, bytes(res, 'utf-8')
