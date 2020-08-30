import random
import numpy as np
from sklearn.neighbors import NearestNeighbors
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import geopandas as gpd
import math
import time


class Agent:
    def __init__(self, env, identity):
        self.identity = identity
        self.env = env
        self.location = self.random_location()
        print(f'This is agent {self.identity}: \n {self.location}')

        # trajectory: 24 hours a day for 14 days. None means not close to any pre-defined locations
        self.trajectory = np.full((14, 24), None)
        self.min_speed = env.min_speed
        self.max_speed = env.max_speed
        self.record_range = env.record_range

        # while True:
        for _ in range(5):
            time.sleep(1)  # should be defined later
            self.move()

    def random_location(self):
        """ generate a point in Singapore boundary.

        Returns:
        Point: Returning value

        """
        border = self.env.simu_map.polys
        long_min, lat_min, long_max, lat_max = border.bounds
        while True:
            location = (random.uniform(
                long_min, long_max), random.uniform(lat_min, lat_max))
            location = Point(location)
            if border.contains(location):
                return location

    def move(self):
        will_move = bool(random.randint(0, 1))
        direction = [random.uniform(0, 1) / math.sqrt(2) for _ in range(2)]
        speed = random.uniform(self.min_speed, self.max_speed)
        # calculate the new location
        self.update()

    def update(self):
        # update the trajectory if the new location is within a certain distance (record_range)
        print('moving! ')
        pass

    def show(self):
        """ Plot the agent in Singapore boundary.

        Return: None

        """
        fig = plt.figure()
        ax = fig.add_subplot(111)
        xs, ys = self.env.simu_map.polys.exterior.xy
        ax.plot(xs, ys, linewidth=1)
        plt.plot(self.location.x, self.location.y, 'ro')
        ax.set_title('Singapore Map')
        plt.show()
