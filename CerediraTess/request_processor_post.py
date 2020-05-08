#!/usr/bin/env python3
# coding=utf-8
"""
:author: gdjamalov@aplana.com, unixshaman@gmail.com
Модуль для хранения статических функций обрабатывающих POST запросы к серверу
"""
import json
import logging

from CerediraTess import utility, server

module_logger = logging.getLogger('CerediraTess.request_processor_post')


def post_response(body):
    """Выполнить указанный запрос HTTP.
    """
    js_receive = json.loads(body.decode('utf-8'))
    return 200, {}, bytes(f'hello world\n{json.dumps(js_receive, indent=4, ensure_ascii=False)}', 'utf8')


def execute_script(script_name, body):
    """
    :param script_name:
    :param body:
    :return:
    """
    logger = logging.getLogger('CerediraTess.get_request_processor.get_file_from_server')
    logger.debug(f'Execute script {script_name}')

    js_receive = json.loads(body.decode('utf-8'))
    args = js_receive['args'] if 'args' in js_receive else []
    encoding = js_receive['encoding'] if 'encoding' in js_receive else 'utf-8'
    timeout = js_receive['timeout'] if 'timeout' in js_receive else 60

    res = utility.run_with_timeout(server.WEB_ROOT, script_name, args, encoding, timeout)
    return 200, {}, bytes(res, 'utf8')


def execute_remote_script(script_name, body):
    js_receive = json.loads(body.decode('utf-8'))
    args = js_receive['args'] if 'args' in js_receive else []
    hostname = js_receive['hostname'] if 'hostname' in js_receive else None
    username = js_receive['username'] if 'username' in js_receive else None
    password = js_receive['password'] if 'password' in js_receive else None
    encoding = js_receive['encoding'] if 'encoding' in js_receive else 'utf-8'
    timeout = js_receive['timeout'] if 'timeout' in js_receive else 60
    res = utility.run_remote_with_timeout(server.WEB_ROOT, script_name, hostname,
                                          {'username': username, 'password': password}, args, encoding, timeout)
    return 200, {}, bytes(res, 'utf8')
