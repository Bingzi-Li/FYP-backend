import math


class Env:
    def __init__(self, simu_map, min_speed=5, max_speed=80):
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.record_range = None
        self.simu_map = simu_map
