from .simulation import Simulation

class Environment:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Environment, cls).__new__(cls)
            cls._instance.sim = Simulation()
        return cls._instance

env = Environment()
