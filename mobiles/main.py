from simulator import env, map, agent
from threading import Thread
import concurrent.futures


class MobileSimulation:
    def __init__(self, n):
        self.env = env.Env()
        self.map = map.Map()
        with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
            executor.submit(agent.Agent(env))


if __name__ == '__main__':
    # MobileSimulation(100)
    pass
