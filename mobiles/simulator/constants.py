'''constants of the simulator module
'''

# Map
FILE_LOC = './mapfiles/SG4/gadm36_SGP_0.shp'
SG_CRS = 3414  # unit: metre

# Simulation
UPDATE_PERIOD = 3600  # unit: s
SIMU_TIMESCALE = 3600  # simulation time / real time
NUM_AGENTS = 50

# Node data
NODE_DATA_LOC = './node_data/mrt_lrt_data.json'

# code mode
DEBUG = False
SIMU_DAYS = 14  # stopping point in debugging mode

# recording frequency
N_PER_DAY = 24
TRACING_DAYS = 14


SERVER_URL = 'http://localhost:5000'
