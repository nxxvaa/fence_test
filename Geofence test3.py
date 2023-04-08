from __future__ import print_function
import time
from dronekit import connect, Command, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil, mavwp
import math
import os
import json
import csv

# Use UDP to connect to the SITL simulator through the local port 14551
connection_string ='127.0.0.1:14551' #'tcp:127.0.0.1:5760'  #
print('Connecting to vehicle on: %s' % connection_string)
# The connect function will return an object of type Vehicle, which is the vehicle here
vehicle = connect(connection_string, wait_ready=True)

class automission(object):
    # docstring for automission
    def __init__(self, vehicle_type):

        super(automission, self).__init__()
        assert vehicle_type == 'plane'
        self.mlist = []  # each element of the array represents a command, ie waypoint, with its parameters
        self.counter = 1

        # these two lines are by default, exists every mission planner file
        #self.mlist.append(f"QGC WPL 110\n0\t1\t0\t16\t0\t0\t0\t0\t{home_lat}\t{home_long}\t{home_ASL}\t1\n") # Current Home Location

    def param_to_mcommand(self,
                          *args):  # takes command and its parameters, appends them to mlist while adjusting formatting
        string = str(self.counter) + '\t'
        self.counter += 1

        for i in args:
            string += str(i) + '\t'
        string = string.rstrip('\t')
        string += '\n'
        self.mlist.append(string)

    ### Mission Commands ###
    # every parameter list begins with '0,3,' and ends with ',1'

    def waypoint(self, lat, lon, alt, delay=0):
        waypoint_id = 16
        self.param_to_mcommand(0, 3, waypoint_id, delay, 0, 0, 0, lat, lon, alt,1)

    def takeoff(self, angle, lat, lon, alt):
        takeoff_id = 22
        self.param_to_mcommand(0, 3, takeoff_id, angle, 0, 0, 0, lat, lon, alt,1)

    def inclusion_fence_vertix(self, points, lat, lon):
        geofence_vertix_inclusion_id = 50001
        self.param_to_mcommand(0, 3, geofence_vertix_inclusion_id, points, 0, 0, 0, lat, lon, 0,1)
    

    def write(self, name='Waypointsedited'):
        # saves final command list mlist as WP file.
        # Missionplanner can direcly open this text document in flight plan / load WP file button
        # open(str(name)+".waypoints", 'w').close()
        with open(str(name) + ".txt", "w") as text_file:
            for i in self.mlist:
                print(i)
                text_file.write(i)


def readmission(aFileName): #Load a mission from a file into a list
    print("\nReading mission from file: %s" % aFileName)
    cmds = vehicle.commands
    missionlist = []
    with open(aFileName) as f:
        for i, line in enumerate(f):
            linearray = line.split('\t')
            ln_index = int(linearray[0])
            ln_currentwp = int(linearray[1])
            ln_frame = int(linearray[2])
            ln_command = int(linearray[3])
            ln_param1 = float(linearray[4])
            ln_param2 = float(linearray[5])
            ln_param3 = float(linearray[6])
            ln_param4 = float(linearray[7])
            ln_param5 = float(linearray[8])
            ln_param6 = float(linearray[9])
            ln_param7 = float(linearray[10])
            ln_autocontinue = int(linearray[11].strip())
            cmd = Command(0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2,
                          ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
            missionlist.append(cmd)
    return missionlist


def upload_mission(aFileName): #Upload a mission from a file
    missionlist = readmission(aFileName) # Read mission from file
    print("\nUpload mission from a file: %s" % aFileName)
    print(' Clear mission')
    cmds = vehicle.commands
    #cmds.clear() # Clear existing mission from vehicle
    # Add new mission to vehicle
    for command in missionlist:
        cmds.add(command)
    print(' Upload mission')
    vehicle.commands.upload()

cmds = vehicle.commands
cmds.download()
cmds.wait_ready()
cmds.clear()
upload_mission('mission.waypoints')