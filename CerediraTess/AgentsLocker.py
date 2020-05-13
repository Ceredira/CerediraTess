import threading


class AgentsLocker:
    def __init__(self, list_of_agents):
        self.list_of_agents = list_of_agents
        self.dict_of_agents = {}
        for agent in self.list_of_agents:
            self.dict_of_agents[agent.hostname] = agent
        self.locking_lock = threading.Lock()

    def agents_lock(self, lock_user, agents_for_lock, lock_cause, min_agents_count, max_agents_count=None):
        locking_result = {}
        if not agents_for_lock:
            agents_for_lock = [x.hostname for x in self.list_of_agents if lock_user in x.users]

        list_of_agents = [x for x in self.list_of_agents if (x.hostname in agents_for_lock) and (lock_user in x.users)]

        if len(list_of_agents) < min_agents_count:
            locking_result = {
                'result': False, 'locked_agents': [],
                'locking_log': f'List of available agents less then minimum agents count {min_agents_count}'
            }
        else:
            self.locking_lock.acquire()
            try:
                check_locking = True
                unlocked_agents = [x for x in list_of_agents if (x.lock_user is None)]

                if len(unlocked_agents) < min_agents_count:
                    locking_result = {
                        'result': False, 'locked_agents': [],
                        'locking_log': f'List of free agents less then minimum agents count {min_agents_count}'
                    }
                    check_locking = False
                else:
                    if max_agents_count is not None:
                        if len(unlocked_agents) < max_agents_count:
                            locking_result = {
                                'result': False, 'locked_agents': [],
                                'locking_log': f'List of free agents less then maximum agents needed count {max_agents_count}'
                            }
                            check_locking = False
                    else:
                        max_agents_count = len(unlocked_agents)

                if check_locking:
                    locked_agents = []
                    locking_log = ''
                    for i in range(max_agents_count):
                        unlocked_agents[i].lock(lock_user, lock_cause)
                        locked_agents.append(unlocked_agents[i].hostname)
                        locking_log += f'Agent {unlocked_agents[i].hostname} locked\n'

                    locking_result = {
                        'result': True, 'locked_agents': locked_agents,
                        'locking_log': locking_log
                    }
            finally:
                self.locking_lock.release()

        return locking_result

    def agents_unlock(self, lock_user, agents_for_unlock, lock_cause):
        unlocking_log = ''
        unlocking_res = True
        unlocking_agents = []

        self.locking_lock.acquire()

        try:
            if not agents_for_unlock:
                agents_for_unlock = [x.hostname for x in self.list_of_agents if (lock_user in x.users) and
                                     (x.lock_cause == lock_cause)]

            for agent_hostname in agents_for_unlock:
                if agent_hostname in self.dict_of_agents:
                    res, log = self.dict_of_agents[agent_hostname].unlock(lock_user, lock_cause)
                    unlocking_res = unlocking_res and res
                    unlocking_log += f'{log}\n'
                    unlocking_agents.append(agent_hostname)
                else:
                    unlocking_log += f'Agent {agent_hostname} does not exists\n'
        finally:
            self.locking_lock.release()

        return {
            "result": True, "unlocking_agents": unlocking_agents,
            "unlocking_log": unlocking_log
        }
