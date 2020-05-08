import time


class Agent:
    lock = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Agent, cls).__new__(cls)
        return cls.instance

    def __init__(self, name):
        self.name = name

    def lock(self):
        while True:
            if not self.lock:
                self.lock = True
                return
            else:
                time.sleep(5)
