from pymavlink import mavutil
from pymavlink.mavextra import *
from pymavlink.dialects.v20 import ardupilotmega as mavlink2

# Create a connection to the vehicle
vehicle = mavutil.mavlink_connection(device="udp:127.0.0.1:14550")

# Wait for the connection to be established
vehicle.wait_heartbeat()

# Open the mission file
with open('mission.waypoints', 'r') as f:
    mission_raw = f.read()

# Send the mission file to the vehicle
# vehicle.mav.mission_write_partial_list_send(
#     0,               # The start index for the mission items
#     0,               # The end index for the mission items (0 indicates all items)
#     len(mission),    # The size of the mission file
#     b'',             # Unused
#     mavutil.mission_string_encode() # The mission file as a byte string
# )
mission = mavutil.mavlink20.mission_encode(mission_raw)

# Send the mission to the vehicle
vehicle.waypoint_send_list_send(
    mission.target_system,  # System ID of the vehicle
    mission.target_component, # Component ID of the vehicle
    mission.waypoints # List of waypoints in MAVLink format
)
# Wait for the mission upload to complete
while True:
    msg = vehicle.recv_match(type='MISSION_ACK', blocking=True)
    if msg.type == mavutil.mavlink.MAV_MISSION_RESULT.MAV_MISSION_ACCEPTED:
        print('Mission upload successful!')
        break
    elif msg.type == mavutil.mavlink.MAV_MISSION_RESULT.MAV_MISSION_ERROR:
        print('Mission upload failed!')
        break
