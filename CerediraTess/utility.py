#!/usr/bin/env python3
# coding=utf-8
"""
:author: unixshaman
Модуль для хранения статических частоиспользуемых функций
"""

import logging
import os
import subprocess
from builtins import Exception

from func_timeout import func_timeout, FunctionTimedOut


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
    text = ""
    with open(filename, mode=mode, encoding='utf-8') as f:
        for line in f:
            text += line

    return text


def run_with_timeout(root_path, script, args_list=[], encoding='utf-8', timeout=60):
    logger = logging.getLogger("CerediraTess.utility.run_with_timeout")
    logger.debug(f'Execute run_with_timeout with args: {root_path}, {script}, {args_list}, {encoding}, {timeout}')
    try:
        return func_timeout(timeout, execute_batch, args=(root_path, script, args_list, encoding))
    except FunctionTimedOut:
        return f"Could not complete within {timeout} seconds and was terminated."
    except Exception as e:
        logger.error("Exception occurred", exc_info=True)
        return f"Error while create process: {e}"


def run_remote_with_timeout(root_path, script, hostname, psexec_options=None, args_list=None, encoding='utf-8',
                            timeout=60):
    logger = logging.getLogger("CerediraTess.utility.run_remote_with_timeout")
    logger.debug(f'Execute run_with_timeout with args: {root_path}, {script}, {args_list}, {encoding}, {timeout}')
    try:
        return func_timeout(timeout, execute_batch_remote,
                            args=(root_path, script, hostname, psexec_options, args_list, encoding))
    except FunctionTimedOut:
        return f"Could not complete within {timeout} seconds and was terminated."
    except Exception as e:
        logger.error("Exception occurred", exc_info=True)
        return f"Error while create process: {e}"


def execute_batch(root_path, script, args_list=[], encoding='utf-8'):
    logger = logging.getLogger("CerediraTess.utility.execute_batch")

    proc = [os.path.join(root_path, 'scripts', script)]
    proc.extend(args_list)

    try:
        with subprocess.Popen(proc, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False) as child:
            with child.stdout as stdout:
                output = stdout.read().decode(encoding, errors='replace')
    except Exception as ex:
        output = f'Exception while execution: {ex}'

    logger.debug(f'Script execution result:\n{output}')

    return output


def execute_batch_remote(root_path, script, hostname, psexec_options=None, args_list=None, encoding='utf-8'):
    logger = logging.getLogger("CerediraTess.utility.execute_batch_remote")

    if args_list is None:
        args_list = []
    if psexec_options is None:
        psexec_options = {}

    proc = [os.path.join(root_path, 'resources\\psexec.exe')]
    if 'username' in psexec_options:
        proc.extend(['-u', psexec_options['username']])
    if 'password' in psexec_options:
        proc.extend(['-p', psexec_options['password']])

    proc.extend([f'\\\\{hostname}', '-accepteula', '-nobanner'])
    proc.extend(['-c', os.path.join(root_path, 'scripts', script)])
    proc.extend(args_list)

    exec_command = ''
    for i in proc:
        exec_command += f'{i} '
    print(exec_command)
    output = None
    try:
        with subprocess.Popen(proc, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False) as child:
            child.wait()
            with child.stdout as stdout:
                output = stdout.read().decode(encoding, errors="replace")
    except Exception as ex:
        output = f'Exception while execution: {ex}'

    logger.debug(f'Script execution result:\n{output}')

    return output
