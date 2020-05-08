import os
from unittest import TestCase

from CerediraTess import utility

WEB_ROOT = os.path.dirname(os.getcwd())


class TestUtility(TestCase):

    def test_execute_batch_work(self):
        res = utility.execute_batch(WEB_ROOT, 'test.bat')
        print(res)
        assert ('asdf' in res) is True, 'Скрипт выполнился'

    def test_execute_batch_check_input_param(self):
        res = utility.execute_batch(WEB_ROOT, 'test.bat', ['ggg'])
        print(res)
        assert ('ggg' in res) is True, 'В результате выполнения содержится входной параметр ggg'

    def test_execute_batch_remote_work(self):
        res = utility.execute_batch_remote(WEB_ROOT, 'test.bat', '192.168.1.189',
                                           {'username': 'unixshaman_15\\unixshaman', 'password': '1qaz@WSX'})
        print(res)
        assert ('asdf' in res) is True, 'Скрипт выполнился'
