lat = 30.0444
lon = 31.2357
alt = 0

# Import pymavlink
from pymavlink import mavutil

# Create a connection object
connection = mavutil.mavlink_connection(device="tcp:127.0.0.1:5762")

# Wait for heartbeat
connection.wait_heartbeat()



connection.mav.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION(3,0,0).send
# msg = connection.mav.command_long_encode(
#     0, # target system
#     0, # sequence number
#     mavutil.mavlink.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION, # command
#     3, # current
#     0, # autocontinue
#     0, # param1
#     0,
#     0, # param2
#     lat, # x (latitude)
#     lon, # param3
#     0) # z (altitude)

# # Send the mission item to the vehicle
# connection.mav.send(msg)
print("done")