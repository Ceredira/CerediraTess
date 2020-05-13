import logging
import os
import subprocess
import threading
from builtins import Exception

from func_timeout import func_timeout, FunctionTimedOut


class Agent:
    def __init__(self, hostname, os_type, description='', users=None, scripts=None):
        if scripts is None:
            scripts = []
        if users is None:
            users = []

        self.hostname = hostname
        self.os_type = os_type
        self.description = description
        self.users = users
        self.scripts = scripts
        self.execution_lock = threading.Lock()
        self.lock_cause = None
        self.lock_user = None

    def lock(self, lock_user, lock_cause):
        if self.lock_user is None:
            self.lock_user = lock_user
            self.lock_cause = lock_cause
            return True, f'Agent {self.hostname} locked'
        elif self.lock_user == lock_user:
            return False, f'Agent {self.hostname} already locked by you, but with a cause: {self.lock_cause}'
        else:
            return False, f'Agent {self.hostname} locked by another user'

    def unlock(self, lock_user, lock_cause):
        if self.lock_user is None:
            return True, f'Agent {self.hostname} already unlocked'
        if self.lock_user == lock_user:
            if self.lock_cause == lock_cause:
                self.lock_user = None
                self.lock_cause = None
                return True, f'Agent {self.hostname} unlocked'
            else:
                return False, f'Cannot unlock agent {self.hostname}, locked with another cause: {self.lock_cause}'
        return False, f'Cannot unlock agent {self.hostname}, locked with another user'

    def execute_script_with_timeout(self, root_path, script, hostname, psexec_options=None, args_list=None,
                                    encoding='utf-8',
                                    timeout=60):
        logger = logging.getLogger("CerediraTess.Agent.execute_script_with_timeout")
        logger.debug(
            f'Execute run_with_timeout with args: {root_path}, {script}, {args_list}, {encoding}, {timeout}')
        try:
            if hostname == 'CerediraTess':
                return func_timeout(timeout, self.execute_script_locally, args=(root_path, script, args_list, encoding))
            else:
                return func_timeout(timeout, self.execute_script_remote,
                                    args=(root_path, script, hostname, psexec_options, args_list, encoding))
        except FunctionTimedOut:
            return f"Could not complete within {timeout} seconds and was terminated."
        except Exception as e:
            logger.error("Exception occurred", exc_info=True)
            return f"Error while create process: {e}"

    @staticmethod
    def execute_script_locally(root_path, script, args_list=None, encoding='utf-8'):
        if args_list is None:
            args_list = []
        logger = logging.getLogger("CerediraTess.Agent.execute_script_locally")

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

    @staticmethod
    def execute_script_remote(root_path, script, hostname, psexec_options=None, args_list=None, encoding='utf-8'):
        logger = logging.getLogger("CerediraTess.Agent.execute_script_remote")

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
