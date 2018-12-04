#!/usr/bin/env python3
"""
Example demonstrating how to communicate with Microsoft Robotic Developer
Studio 4 via the Lokarria http interface.

Author: Erik Billing (billing@cs.umu.se)

Updated by Ola Ringdahl 2014-09-11
Updated by Lennart Jern 2016-09-06 (converted to Python 3)
Updated by Filip Allberg and Daniel Harr 2017-08-30 (actually converted to Python 3)
Updated by Ola Ringdahl 2017-10-18 (added example code that use showMap)
Updated by Ola Ringdahl 2018-11-01 (fixed so that you can write the address with http://
    without getting a socket error. Added a function for converting (x,y) to (row,col))
"""

import time

from deliberativeLayer.cartographer.map_info import Cspace
from deliberativeLayer.cartographer.show_map import *
from deliberativeLayer.frontierBasedExploration.frontierCalculator import *
from reactiveLayer.sensing.robotMovement import *
from reactiveLayer.sensing.robotSensing import *

url = 'http://localhost:50000'
# HTTPConnection does not want to have http:// in the address apparently, so lest's remove it:
MRDS_URL = url[len("http://"):]
HEADERS = {"Content-type": "application/json", "Accept": "text/json"}


class UnexpectedResponse(Exception):
    pass


def calculate_distance(x1,y1,x2,y2):
    return (abs(x1-x2)**2+abs(y1-y2)**2)**0.5



if __name__ == '__main__':

    showGUI = True  # set this to False if you run in putty

    # Max grid value
    maxVal = 15
    cell_size = 1

    print('Sending commands to MRDS server', MRDS_URL)

    c_space = Cspace(-15, -15, 15, 15, cell_size)
    bayes_map = Bayesian(c_space.occupancy_grid)
    map = ShowMap(c_space.grid_nr_rows, c_space.grid_nr_columns, showGUI)
    robot_sensing = robotSensing()
    frontier_calculator = frontierCalculator()

    try:
        print('Telling the robot to go straight ahead.')
        response = postSpeed(0, 0.2)

        while(1):
            #print('in while!')

            # Get all the laser readout values starting from
            # the one with angle 0 to 270 (in meters)
            laser_scan_values = robot_sensing.get_laser_scan()

            # Get all the laser angles starting from 0 to 270
            laser_angles = robot_sensing.get_laser_angles()

            # Converts the car's (x, y) position to (row, col) coordinate in the grid
            pose = getPose()
            curr_pos = pose['Pose']['Position']

            robot_coord = pos_to_grid(curr_pos['X'], curr_pos['Y'], c_space.x_min, c_space.y_max, cell_size)
            robot_row = robot_coord[0]
            robot_col = robot_coord[1]
            #print('Im at coordinate', robot_coord) # These are floats! Not integers!

            # Retrieve the angles needed to calculate
            orientation=getOrientation()

            # Calculate the coordinates laser point readings
            sensor_readout_coordinates = robot_sensing.get_sensor_readout_coordinates(robot_coord,
                laser_scan_values['Echoes'], laser_angles, orientation)

            # Get all the Bresenham lines
            bresenham_lines = robot_sensing.get_bresenham_lines(robot_coord, sensor_readout_coordinates)



            for bresenham_line in bresenham_lines:
                # Calculate the distance from the robot coordinate to the end point of each Bresenham line
                #dist = calculate_distance(bresenham_line[-1][0],bresenham_line[-1][1],robot_row,robot_col)
                #                          bresenham_lines[len(bresenham_lines) - 1][1],robot_row,robot_col)

                bayes_map.bayes_handler(bresenham_line, robot_row, robot_col)
                """
                for coordinate in bresenham_line:
                    #pos_to_grid(coordinate[0], coordinate[1], c_space.x_min, c_space.y_max, cell_size)
                    if math.floor(coordinate[0]) < c_space.grid_nr_rows and math.floor(coordinate[1]) < c_space.grid_nr_columns and \
                       math.floor(coordinate[0]) >= 0 and math.floor(coordinate[1]) >= 0:
                        c_space.occupancy_grid[math.floor(coordinate[0])][math.floor(coordinate[1])] = 0


            fontiers = frontier_calculator.find_frontiers(c_space, robot_coord)
            """
            #print(fontiers)

            #print('updating map')

            map.updateMap(c_space.occupancy_grid, maxVal, robot_row, robot_col, orientation)

    except UnexpectedResponse as ex:
        print('Unexpected response from server when sending speed commands:', ex)