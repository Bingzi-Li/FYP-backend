import random
import numpy as np
from sklearn.neighbors import NearestNeighbors
import math
import time


class Agent:
    def __init__(self, env):
        # need to confine the points to Singapore boundary
        self.location = [random.uniform(-180, 180), random.uniform(-90, 90)]
        # trajectory: 24 hours a day for 14 days. None means not close to any pre-defined locations
        self.trajectory = np.full((14, 24), None)
        self.min_speed = env.min_speed
        self.max_speed = env.max_speed
        self.record_range = env.record_range
        while True:
            time.sleep(1)  # should be defined later
            self.move()

    def move(self):
        will_move = bool(random.randint(0, 1))
        direction = [random.random(0, 1) / math.sqrt(2) for _ in range(2)]
        speed = random.random(self.min_speed, self.max_speed)
        # calculate the new location
        self.update()

    def update(self):
        # update the trajectory if the new location is within a certain distance (record_range)
        pass
