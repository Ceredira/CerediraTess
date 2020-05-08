#!/usr/bin/env python3
# coding=utf-8
"""
:author: gdjamalov@aplana.com, unixshaman@gmail.com
Модуль для хранения статических функций обрабатывающих GET запросы к серверу
"""

import logging
import os

from CerediraTess import utility

module_logger = logging.getLogger('CerediraTess.request_processor_get')


def get_file_from_server(file_path):
    """Функция возвращающая содержимое файла по указанному пути, если пути не существует,
    возвращается код ошибки 404 с ошибкой в теле ответа."""
    logger = logging.getLogger('CerediraTess.get_request_processor.get_file_from_server')
    logger.info(f'Get file from server {file_path}')
    body = bytes()
    if os.path.isfile(file_path):
        for line in utility.retrieve_file(file_path, mode='rb'):
            body += line
        file_ext = str(file_path.split('.')[-1])
        if file_ext == 'css' or 'html':
            content_type = 'text/' + file_ext
        else:
            content_type = 'text/plain'
        return 200, {'Content-Type': content_type}, body
    else:
        return 404, {}, bytes(f'Запрашиваемый файл {file_path} не существует', 'utf8')
