from pymavlink import mavutil

# Connect to the vehicle
vehicle = mavutil.mavlink_connection(device="udp:127.0.0.1:14550")

# Wait for the heartbeat message to find the system ID
vehicle.wait_heartbeat()

# Create a new mission
# cmds = vehicle.mav.mission_clear_all_send()
# cmds = vehicle.mav.mission_count_send(0, 0)
# cmds = vehicle.mav.mission_item_send(
    # 0, 0,  # target system, target component
    # 0,     # sequence
    # mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    # mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    # 0,  # current
    # 1,  # autocontinue
    # 0, 0, 0, 0,
    # -35.363261,
    # 149.165230,
    # 20)

cmds = vehicle.mav.mission_item_send(
    0, 0,  # target system, target component
    1,     # sequence
    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    mavutil.mavlink.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION,
    0,  # current
    1,  # autocontinue
    3,  #Vertex count
    0,  #Inclusion Group
    0, 0,
    -35.362998,
    149.165327,
    0)

# cmds = vehicle.mav.mission_item_send(
    # 0, 0,  # target system, target component
    # 2,     # sequence
    # mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    # mavutil.mavlink.MAV_CMD_NAV_LAND,
    # 0,   # current
    # 1,   # autocontinue
    # 0,   # param1
    # 0,   # param2
    # 0,
    # 0,   # param3
    # float('nan'),   # param4 - latitude of landing zone (not used)
    # float('nan'),   # param5 - longitude of landing zone (not used)
    # float('nan'))   # param6 - altitude of landing zone (not used)

vehicle.mav.send(cmds)

vehicle.close()