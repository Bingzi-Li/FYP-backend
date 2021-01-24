import random
import sgt
from sgt import SGT
import requests
import numpy as np
from sklearn.neighbors import NearestNeighbors
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import geopandas as gpd
import math
import time
from .constants import SIMU_TIMESCALE, UPDATE_PERIOD, DEBUG, SERVER_URL


class Agent:
    def __init__(self, env, identity, current_time=0):
        self.identity = identity
        self.env = env
        # trajectory: 24 hours a day for 14 days. -1 means not close to any pre-defined locations
        self.trajectory = np.full((14, 24), -1)
        # The current time: which hour
        self.current_time = current_time
        self.min_speed = env.min_speed
        self.max_speed = env.max_speed
        self.record_range = env.record_range

        self.location = self.random_location()
        self.update()
        print(f'This is agent {self.identity}: \n {self.location}')

        if DEBUG:
            # ----plot the tracjectory
            fig = plt.figure()
            ax = fig.add_subplot(111)
            xs, ys = self.env.simu_map.polys.exterior.xy
            ax.plot(xs, ys, linewidth=1)
            # --- debug counter
            debug_counter = 0

        while True:
            # sleep for a simu time
            time.sleep(UPDATE_PERIOD / SIMU_TIMESCALE)
            self.move()
            self.update()
            # update the current time: day + 1
            self.current_time += 1
            if self.current_time > self.env.simu_time:
                print(f'Agent {self.identity} time up! {self.current_time}')
                break

            if DEBUG:
                # --- plot the trajectory
                plt.plot(self.location.x, self.location.y, 'ro')
                # --- debug counter
                debug_counter += 1
                if debug_counter > 24:
                    break
        if DEBUG:
            # --- plot the trajectory
            # self.plot_station(plt)
            for node in self.env.nodes:
                plt.plot(node['point'].x, node['point'].y, 'b+')
            ax.set_title('Singapore Map')
            plt.show()
        print(self.trajectory)

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
        print(f'Agent {self.identity} will move: {will_move}')
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
        min_dist, node_idx = float('inf'), -1
        # print(self.env.nodes)
        for node in self.env.nodes:
            dist = node['point'].distance(self.location)
            if dist < self.env.record_range and dist < min_dist:
                min_dist = dist
                node_idx = node['id']
        day = self.current_time // 24 % 14
        hour = self.current_time % 24
        if node_idx:
            self.trajectory[day, hour] = node_idx
        # embed and send the data once a day to server
        if hour == 23:
            self.embedding(day)

        print(
            f'Agent {self.identity} moved to node: {node_idx}, location: {self.location}')

    def embedding(self, day):
        '''
        Do the embedding every day and send to the server
        '''
        data = self.trajectory[day, :]
        alphabets = range(-1, len(self.env.nodes))
        sgt = SGT(alphabets=alphabets, flatten=True)
        vector = sgt.fit(data).to_json(orient='values')
        # TODO: send to the server
        data = {'day': day, 'embedding': vector}
        r = requests.post(
            f'{SERVER_URL}/embedding?id={self.identity}', json=data)
        print(r.text)

    def plot_station(self, plt):
        for node in self.env.nodes:
            plt.plot(node['point'].x, node['point'].y, 'b+')

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
