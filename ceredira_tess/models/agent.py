import logging
import os
import subprocess
import traceback

from ceredira_tess.db import db
from ceredira_tess.models import relationships


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hostname = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text)
    lock_cause = db.Column(db.Text)

    lock_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lock_user = db.relationship('User', backref=db.backref('agents', lazy='dynamic'))

    operationsystemtype_id = db.Column(db.Integer, db.ForeignKey('operation_system_type.id'),
                                       nullable=False)
    operationsystemtype = db.relationship('OperationSystemType', backref=db.backref('agents', lazy='dynamic'))
    scripts = db.relationship('Script', secondary=relationships.agents_scripts)
    roles = db.relationship("Role", secondary=relationships.roles_agents, back_populates='agents')

    def __repr__(self):
        return f'{self.hostname}'

    def __init__(self, hostname, operationsystemtype):
        self.hostname = hostname
        self.operationsystemtype = operationsystemtype

    def add_role(self, role):
        self.roles.append(role)

    def lock(self, lock_user, lock_cause):
        list_of_agents = [agent for x in lock_user.roles for agent in x.agents]
        if self in list_of_agents:
            if self.lock_user is None:
                self.lock_user = lock_user
                self.lock_cause = lock_cause
                db.session.commit()
                return True, f'Agent {self.hostname} locked'
            elif self.lock_user == lock_user:
                return False, f'Agent {self.hostname} already locked by you, but with a cause: {self.lock_cause}'
            else:
                return False, f'Agent {self.hostname} locked by another user'
        else:
            return False, f'User cannot access to agent {self.hostname}'

    def unlock(self, lock_user, lock_cause):
        list_of_agents = [agent for x in lock_user.roles for agent in x.agents]
        if self in list_of_agents:
            if self.lock_user is None:
                return True, f'Agent {self.hostname} already unlocked'
            if self.lock_user == lock_user:
                if self.lock_cause == lock_cause:
                    self.lock_user = None
                    self.lock_cause = None
                    db.session.commit()
                    return True, f'Agent {self.hostname} unlocked'
                else:
                    return False, f'Cannot unlock agent {self.hostname}, locked with another cause: {self.lock_cause}'
            return False, f'Cannot unlock agent {self.hostname}, locked with another user'
        else:
            return False, f'User cannot access to agent {self.hostname}'

    def execute_script_with_timeout(self, root_path, script, psexec_options=None, args_list=None,
                                    encoding='utf-8',
                                    timeout=60):
        logger = logging.getLogger("CerediraTess.Agent.execute_script_with_timeout")
        logger.debug(
            f'Execute run_with_timeout with args: {root_path}, {script}, {args_list}, {encoding}, {timeout}')
        try:
            if self.hostname == 'CerediraTess':
                return self.execute_script_locally(root_path, script, args_list, encoding, timeout)
            else:
                return self.execute_script_remote(root_path, script, psexec_options, args_list, encoding,
                                                  timeout)
        except Exception as e:
            logger.error("Exception occurred", exc_info=True)
            return f"Error while create process: {e}"

    def execute_script_locally(self, root_path, script, args_list=None, encoding='utf-8', timeout=60):
        if args_list is None:
            args_list = []
        logger = logging.getLogger("CerediraTess.Agent.execute_script_locally")

        # proc = [os.path.join(root_path, 'scripts', script)]
        # proc.extend(args_list)
        proc = r'{}'.format(os.path.join(root_path, 'scripts', script))

        for i in args_list:
            proc += r' "{}"'.format(f"{i}".replace('"', '""'))

        output = self.exec_proc(proc, encoding, timeout)

        logger.debug(f'Script execution result:\n{output}')

        return output

    def execute_script_remote(self, root_path, script, psexec_options=None, args_list=None, encoding='utf-8',
                              timeout=60):
        logger = logging.getLogger("CerediraTess.Agent.execute_script_remote")

        try:
            args_list = args_list if not None else []
            psexec_options = psexec_options if not None else {}

            if self.operationsystemtype.osname == 'Windows':
                proc = '{prog} \\\\{hostname} {username} {password} -accepteula -nobanner -f -c {script} {script_args}'.format(
                    prog=os.path.join(root_path, 'resources\\psexec.exe'),
                    hostname=self.hostname,
                    username=f"-u {psexec_options['username']}" if 'username' in psexec_options and psexec_options['username'] is not None else '',
                    password=f"-p {psexec_options['password']}" if 'password' in psexec_options and psexec_options['password'] is not None else '',
                    script=os.path.join(root_path, 'scripts', script),
                    script_args=args_list
                )
                output = self.exec_proc(proc, encoding, timeout)
            else:
                script_name = script.split('\\')[-1]
                if 'username' not in psexec_options or psexec_options['username'] is None:
                    raise Exception("Имя пользователя должно быть обязательно указано в параметре username")
                if 'password' not in psexec_options or psexec_options['password'] is None:
                    raise Exception("Пароль пользователя должен быть обязательно указан в параметре password")

                # Скопировать скрипт для выполнения на удаленную машину
                proc1 = self.generate_linux_cmd(os.path.join(root_path, 'resources\\pscp.exe'),
                                                psexec_options['port'] if 'port' in psexec_options else None,
                                                psexec_options['username'], psexec_options['password'],
                                                '', os.path.join(root_path, 'scripts', script), f"{self.hostname}:/tmp")
                output = proc1.replace(psexec_options['password'], '*****') + '\n'
                check_load = self.exec_proc(proc1, encoding, timeout)
                output += check_load + '\n\n'
                if ' | 100%' in check_load:
                    # Указание разрешения на выполнение скрипта на удаленной машине
                    proc2 = self.generate_linux_cmd(os.path.join(root_path, 'resources\\plink.exe'),
                                                    psexec_options['port'] if 'port' in psexec_options else None,
                                                    psexec_options['username'], psexec_options['password'],
                                                    self.hostname, 'chmod', f"+x /tmp/{script_name}")
                    output += proc2.replace(psexec_options['password'], '*****') + '\n'
                    check_chmod = self.exec_proc(proc2, encoding, timeout)
                    output += check_chmod + '\n\n'
                    if not check_chmod:
                        # Выполнение скрипта на удаленной машине
                        proc3 = self.generate_linux_cmd(os.path.join(root_path, 'resources\\plink.exe'),
                                                        psexec_options['port'] if 'port' in psexec_options else None,
                                                        psexec_options['username'], psexec_options['password'],
                                                        self.hostname, f"/tmp/{script_name}", " ".join(args_list))
                        output += proc3.replace(psexec_options['password'], '*****') + '\n'
                        output += self.exec_proc(proc3, encoding, timeout) + '\n\n'

                        proc4 = self.generate_linux_cmd(os.path.join(root_path, 'resources\\plink.exe'),
                                                        psexec_options['port'] if 'port' in psexec_options else None,
                                                        psexec_options['username'],
                                                        psexec_options['password'],
                                                        self.hostname, 'rm', f"/tmp/{script_name}")
                        output += proc4.replace(psexec_options['password'], '*****') + '\n'
                        check_remove = self.exec_proc(proc4, encoding, timeout)

                        if check_remove != '':
                            output += f"\nОшибка удаления файла скрипта с удаленной машины: {check_remove}"
                    else:
                        print(traceback.format_exc())
                        raise Exception(f"Не удалось выдать разрешение на выполнение для скрипта на удаленной машине: {output}")
                else:
                    print(traceback.format_exc())
                    raise Exception(f"Не удалось скопировать скрипт на удаленную машину: {output}")
        except Exception as ex:
            print(traceback.format_exc())
            output = f"Не удалось выполнить запуск скрипта на удаленной машине: {ex}"
            logger.error(output, exc_info=True)

        return output

    def generate_linux_cmd(self, prog, port, username, password, hostname, script, args):
        cmd = '"{prog}" -P {port} -l "{username}" -pw "{password}" -noagent -2 -4 -batch {hostname} "{script}" {args}'.format(
            prog=prog,
            port=port if port is not None else 22,
            username=username,
            password=password,
            script=script,
            hostname=hostname,
            args=args
        )
        logger = logging.getLogger("CerediraTess.Agent.generate_linux_cmd")
        logger.info(cmd.replace(f"-pw \"{password}\"", '*****'))
        return cmd

    def exec_proc(self, proc, encoding, timeout):
        logger = logging.getLogger("CerediraTess.Agent.exec_proc")
        logger.info(proc)
        try:
            output = subprocess.check_output(proc, encoding=encoding, timeout=timeout, stderr=subprocess.STDOUT,
                                             errors='replace')
        except subprocess.CalledProcessError as grepexc:
            output = f'Finish with error: {grepexc.returncode}\n\n{grepexc.output}'
        except Exception as ex:
            output = f'Exception while execution: {ex}'

        logger.debug(f'Script execution result:\n{output}')

        return output
