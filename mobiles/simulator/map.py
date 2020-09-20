from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from .constants import FILE_LOC, SG_CRS
import sys


class Map:
    def __init__(self):
        # define a Singapore map boundary
        data = gpd.read_file(FILE_LOC).to_crs(epsg=SG_CRS)
        # multi polygon, 27th is the outline.
        self.polys = data.loc[0].geometry[27]

        # The set of recording points on the map

    def show(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        xs, ys = self.polys.exterior.xy
        ax.plot(xs, ys, linewidth=1)
        ax.set_title('Singapore Map')
        plt.show()


if __name__ == '__main__':
    map = Map()
    map.show()
