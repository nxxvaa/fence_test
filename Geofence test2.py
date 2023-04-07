# lat = 30.0444
# lon = 31.2357
# alt = 0

from dronekit import connect, VehicleMode,mavutil
from pymavlink.dialects.v20 import ardupilotmega as mavlink
import time

connection_string ='127.0.0.1:14550' #'tcp:127.0.0.1:5760'  #
print('Connecting to vehicle on: %s' % connection_string)
# The connect function will return an object of type Vehicle, which is the vehicle here
vehicle = connect(connection_string, wait_ready=True)
vehicle.commands.clear()

waypoint1 = (37.4219999, -122.0840575, 0)
waypoint2 = (38.4219999, -125.0839575, 0)
waypoint3 = (39.4218999, -124.0839575, 0)
waypoint4 = (36.4218999, -123.0840575, 0)

cmds = vehicle.commands
cmds.clear()

# vehicle.commands.add(
#     mavlink.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION,
#     3,
#     0,
#     0,
#     4,
#     0,
#     0,
#     waypoint1[0],
#     waypoint1[1],
#     0
# )

# time.sleep(1)

cmd = Command( 0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavlink.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION,3,0, 0, 0, waypoint1[0], waypoint1[1], 0)
# time.sleep(1)

# vehicle.commands.add(
#     mavlink.MAV_CMD_NAV_FENCE_POINT_INCLUSION,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     waypoint3[0],
#     waypoint3[1],
#     waypoint3[2],
#     0    
# )
cmds.add(cmd)
cmds.upload()