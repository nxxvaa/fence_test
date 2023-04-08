from pymavlink import mavutil
from pymavlink.mavextra import *
from pymavlink.dialects.v20 import ardupilotmega as mavlink2

# Connect to the vehicle
connection = mavutil.mavlink_connection(device="udp:127.0.0.1:14550")

# Wait for the connection to be established
connection.wait_heartbeat()


with open('mission.txt', 'r') as f:
    mission_items = f.readlines()

# Send the mission items
for item in mission_items:
    msg = mavutil.mavlink.MAVLinkMessage(
        mavutil.mavlink.MAVLINK_MSG_ID_MISSION_ITEM_INT,
        mavutil.mavlink.MAVLINK_MSG_ID_MISSION_ITEM_INT_LEN,
        item.encode()
    )
    connection.mav.send(msg)

# Request a mission acknowledgement message
msg = connection.mav.mission_ack_encode(0, 0, mavutil.mavlink.MAV_MISSION_ACCEPTED)
connection.mav.send(msg)