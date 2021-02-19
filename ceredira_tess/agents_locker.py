import threading


class AgentsLocker:
    """
    Class for thread safe operations with agents for lock, unlock and get status of agents
    """

    def __init__(self):
        """
        Initialize agentsLocker
        """
        self.locking_lock = threading.Lock()

    def agents_lock(self, lock_user, agents_for_lock, lock_cause, min_agents_count, max_agents_count=None):
        """
        Locking agents for user with specific cause

        :param lock_user: username for lock
        :param agents_for_lock:
        :param lock_cause: cause of locking
        :param min_agents_count: minimum required agents count
        :param max_agents_count: maximum required agents count, if None lock all available agents for lock
        :return: dict with locking result, locking text log and list of locked agents hostname
        """
        locking_log = ''  # Locking log
        locking_res = True  # Locking result, False if required agents cannot be locked
        locked_agents = []  # List of locked agents

        self.locking_lock.acquire()
        list_of_agents = [agent for x in lock_user.roles for agent in x.agents]
        dict_of_agents = {}
        for agent in list_of_agents:
            dict_of_agents[agent.hostname] = agent

        try:
            if not agents_for_lock:
                # Get all agents, available for lock by specified user
                # agents_for_lock = [x.hostname for x in self.list_of_agents if (lock_user in x.users)]
                agents_for_lock = list_of_agents

            agents_available_for_lock = len([x.hostname for x in list_of_agents if
                                             (x.lock_user is None) and  # not locked agents
                                             (x.hostname in agents_for_lock)  # agents from required list
                                             ]
                                            )

            if max_agents_count is None:
                max_agents_count = agents_available_for_lock

            if min_agents_count <= agents_available_for_lock >= max_agents_count:
                if max_agents_count >= min_agents_count:
                    for agent_hostname in agents_for_lock:
                        if agent_hostname in dict_of_agents:
                            res, log = dict_of_agents[agent_hostname].lock(lock_user, lock_cause)
                            locking_log += f'{log}\n'
                            if res:
                                locked_agents.append(agent_hostname)
                            if len(locked_agents) >= max_agents_count:
                                break
                        else:
                            locking_log += f'Agent {agent_hostname} does not exists\n'
                else:
                    locking_log += f'maxAgentsCount {max_agents_count} cannot be less then ' \
                                   f'minAgentsCount {min_agents_count}'
                    locking_res = False
            else:
                locking_log += f'Not enough agents to lock. Available {agents_available_for_lock}, ' \
                               f'required {min_agents_count} - {max_agents_count}\n'
                locking_res = False
        finally:
            self.locking_lock.release()

        return {
            "result": locking_res, "locked_agents": locked_agents,
            "locking_log": locking_log
        }

    def agents_unlock(self, lock_user, agents_for_unlock, lock_cause):
        """
        Unlocking agents for user with specific cause

        :param lock_user: username for unlock
        :param agents_for_unlock: list of agents hostname
        :param lock_cause: cause of locking, for protect from unlock from another requests
        :return: dict with unlocking result, unlocking text log and list of unlocked agents hostname
        """
        unlocking_log = ''  # Unlocking log
        unlocking_res = True  # Unlocking result, False if any agent unlock error
        unlocked_agents = []  # List of unlocked agents

        self.locking_lock.acquire()
        list_of_agents = [agent for x in lock_user.roles for agent in x.agents]
        dict_of_agents = {}
        for agent in list_of_agents:
            dict_of_agents[agent.hostname] = agent

        try:
            if not agents_for_unlock:
                # Get all agents, available for unlock by specified user, with specified cause
                agents_for_unlock = [x.hostname for x in list_of_agents if (lock_user in x.users) and
                                     (x.lock_cause == lock_cause)]

            for agent_hostname in agents_for_unlock:
                if agent_hostname in dict_of_agents:
                    res, log = dict_of_agents[agent_hostname].unlock(lock_user, lock_cause)
                    unlocking_res = unlocking_res and res
                    unlocking_log += f'{log}\n'
                    unlocked_agents.append(agent_hostname)
                else:
                    unlocking_log += f'Agent {agent_hostname} does not exists\n'
        finally:
            self.locking_lock.release()

        return {
            "result": unlocking_res, "unlocked_agents": unlocked_agents,
            "unlocking_log": unlocking_log
        }

    def agents_status(self, lock_user, agents_for_statuses):
        self.locking_lock.acquire()
        list_of_agents = [agent for x in lock_user.roles for agent in x.agents]
        try:
            if not agents_for_statuses:
                agents_for_statuses = [x.hostname for x in list_of_agents]
            all_agents = [x for x in list_of_agents if x.hostname in agents_for_statuses]
        finally:
            self.locking_lock.release()
        return all_agents
