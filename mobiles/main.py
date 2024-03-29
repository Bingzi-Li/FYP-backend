from simulator import Env, Map, Agent
from threading import Thread
from simulator.constants import DEBUG, SIMU_DAYS, NUM_AGENTS, N_PER_DAY
import concurrent.futures


class MobileSimulation:
    def __init__(self, n):
        self.simu_map = Map.Map()
        self.env = Env.Env(self.simu_map, simu_time=SIMU_DAYS*N_PER_DAY)
        if DEBUG:
            Agent.Agent(self.env, 0)
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
                results = [executor.submit(Agent.Agent, self.env, i)
                           for i in range(n)]


if __name__ == '__main__':
    MobileSimulation(NUM_AGENTS)
