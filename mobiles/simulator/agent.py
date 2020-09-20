import random
import numpy as np
from sklearn.neighbors import NearestNeighbors
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import geopandas as gpd
import math
import time
from .constants import SIMU_TIMESCALE, UPDATE_PERIOD


class Agent:
    def __init__(self, env, identity):
        self.identity = identity
        self.env = env
        # trajectory: 24 hours a day for 14 days. None means not close to any pre-defined locations
        self.trajectory = np.full((15, 24), None)
        # The current time: which day, which hour
        self.current_time = [0, 0]
        self.min_speed = env.min_speed
        self.max_speed = env.max_speed
        self.record_range = env.record_range

        self.location = self.random_location()
        self.update()
        print(f'This is agent {self.identity}: \n {self.location}')

        while True:
            # for _ in range(5):
            time.sleep(UPDATE_PERIOD / SIMU_TIMESCALE)
            # update the current time
            if self.current_time[1] == 23:
                self.current_time[1] = 0
                self.current_time[0] += 1
            else:
                self.current_time[1] += 1
            self.move()
            self.update()

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
        if will_move:
            radian = random.uniform(-1.58, 1.58)
            direction = (math.sin(radian), 1 - math.sin(radian)**2)
            dist = random.uniform(
                self.min_speed, self.max_speed) * UPDATE_PERIOD
            # calculate the new location, make sure it's  in SG map
            new_loc = Point(self.location.x + dist *
                            direction[0], self.location.y + dist * direction[1])
            while not self.env.simu_map.polys.contains(new_loc):
                radian = random.uniform(-1.58, 1.58)
                direction = (math.sin(radian), 1 - math.sin(radian)**2)
                dist = random.uniform(
                    self.min_speed, self.max_speed) * UPDATE_PERIOD
                new_loc = Point(
                    self.location.x + dist * direction[0], self.location.y + dist * direction[1])

            self.location = new_loc

    def update(self):
        '''
        update the trajectory if the new location is within a certain distance (record_range) of a node.
        if there are several nodes in the range, update the trajectory to be the nearest one 
        '''
        min_dist, node_idx = float('inf'), None
        for idx, node in self.env.nodes:
            dist = node['point'].distance(self.location)
            if dist < self.env.record_range and dist < min_dist:
                min_dist = dist
                node_idx = idx
        if idx:
            self.trajectory[self.current_time[0] %
                            15, self.current_time[1]] = node_idx

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
