#!/usr/bin/env python3
# coding=utf-8
"""
:author: unixshaman
Модуль для хранения статических частоиспользуемых функций
"""

import logging
import os
import re

from CerediraTess.agent import Agent
from CerediraTess.user import User


def retrieve_file(filename, mode='r'):
    """Функция возвращает генератор списка строк объекта файла"""
    logger = logging.getLogger("CerediraTess.utility.retrieve_file")
    logger.info("retrieve_file {0} with mode {1}".format(filename, mode))
    with open(filename, mode=mode) as f:
        for line in f:
            yield line


def retrieve_file_as_string(filename, mode='r'):
    """Функция возвращает строку"""
    logger = logging.getLogger("CerediraTess.utility.retrieve_file_as_string")
    logger.info("retrieve_file_as_string {0} with mode {1}".format(filename, mode))

    with open(filename, mode=mode, encoding='utf-8') as f:
        text = f.read()

    return text


def encode_complex(o):
    if isinstance(o, Agent):
        return {'hostname': o.hostname, 'os_type': o.os_type, 'description': o.description, 'users': o.users, 'scripts': o.scripts}
    elif isinstance(o, User):
        return {'username': o.username, 'salt': o.salt, 'key': o.key}
    else:
        type_name = o.__class__.__name__
        raise TypeError(f'Object of type "{type_name}" is not JSON serializable')


def encode_agent(o):
    if isinstance(o, Agent):
        return {'hostname': o.hostname, 'lock_cause': o.lock_cause, 'lock_user': o.lock_user}
    else:
        type_name = o.__class__.__name__
        raise TypeError(f'Object of type "{type_name}" is not JSON serializable')


def decode_complex(dct):
    if 'hostname' in dct:
        return Agent(dct['hostname'], dct['os_type'], dct['description'], dct['users'], dct['scripts'])
    elif 'username' in dct:
        if 'salt' in dct and 'key' in dct:
            return User(dct['username'], dct['salt'], dct['key'])
        else:
            return User(dct['username'])
    return dct


def parse_script_metadata(root_path, script):
    with open(os.path.join(root_path, 'scripts', script), encoding='utf-8') as script_file:
        script_content = script_file.read()

    script_description = re.findall(r'REM SCRIPT DESCRIPTION: (.*)', script_content)
    script_args_desc = re.findall(r'REM ARG DESCRIPTION: (.*)', script_content)
    script_args_example = re.findall(r'REM ARG EXAMPLE: (.*)', script_content)

    result = {
        script: {
            'description': '\n'.join(script_description),
            'arguments': script_args_example,
            'argumentsDescription': script_args_desc
        }
    }
    return result
