import math
from .constants import NODE_DATA_LOC, SG_CRS
import json
from pyproj import Proj, transform
from shapely.geometry import Point, Polygon


class Env:
    def __init__(self, simu_map, min_speed=0, max_speed=14):
        '''
        speed: m/s
        '''
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.record_range = 2000
        self.simu_map = simu_map
        self.nodes = self.get_nodes()

    def get_nodes(self):
        nodes = []
        with open(NODE_DATA_LOC) as json_file:
            data = json.load(json_file)
            in_proj = Proj('epsg:4326')
            out_proj = Proj('epsg:' + str(SG_CRS))
            for each in data:
                node = {}
                node['name'] = each['station_name']
                # the new transform seems to accept (lat, long) but our crs point is (long, lat)
                y, x = transform(in_proj, out_proj,  each['lat'], each['lng'])
                node['point'] = Point(x, y)
                nodes.append(node)
        return nodes
