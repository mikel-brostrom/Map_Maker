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

from deliberativeLayer.cartographer.show_map import *
from deliberativeLayer.frontierBasedExploration.frontierCalculator import*
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
    # use the same no. of rows and cols in map and grid:
    nRows = 200
    nCols = 300
    # Initialize a ShowMap object. Do this only once!!
    map = ShowMap(nRows, nCols, showGUI)
    # create an occupancy grid with all cells set to 7 (unexplored) as
    # numpy matrix:
    occupancy_grid = np.ones(shape=(nRows, nCols)) * 7
    # create a probability grid with all cells set to 0.5 (same probability of being exampled
    # as unexplored) as numpy matrix:
    probability_grid = np.ones(shape=(nRows, nCols)) * 0.5
    # or as a two-dimensional array:
    # grid = [[7 for col in range(nCols)] for row in range(nRows)]
    # create some obstacles (black/grey)
    # Upper left side:

    # An explored area (white)
    for rw in range(35, 50):
        for cl in range(32, 55):
            occupancy_grid[rw][cl] = 7


    # Max grid value
    maxVal = 15

    # Hard coded values for max/min x,y
    min_x = -15
    max_y = 15
    cell_size = 0.1

    print('Sending commands to MRDS server', MRDS_URL)
    print('Fuck maps\n')

    robot_sensing = robotSensing()
    frontier_calculator = frontierCalculator()

    try:
        print('Telling the robot to go straight ahead.')
        response = postSpeed(1, -1)

        while(1):

            # Get all the laser readout values starting from
            # the one with angle 0 to 270 (in meters)
            laser_scan_values = robot_sensing.get_laser_scan()
            # Get all the laser angles starting from 0 to 270
            laser_angles = robot_sensing.get_laser_angles()

            # Converts the car's (x, y) position to (row, col) coordinate in the grid
            pose = getPose()
            curr_pos = pose['Pose']['Position']
            robot_coord = pos_to_grid(curr_pos['X'], curr_pos['Y'], min_x, max_y, cell_size)
            robot_row = robot_coord[0]
            robot_col = robot_coord[1]
            #print('Im at coordinate', robot_coord) # These are floats! Not integers!

            # Retrieve the angles needed to calculate
            orientation=getOrientation();

            # Calculate the coordinates laser point readings
            sensor_readout_coordinates = robot_sensing.get_sensor_readout_coordinates(robot_coord,\
                laser_scan_values['Echoes'], laser_angles, orientation)

            # Get all the Bresenham lines
            bresenham_lines = robot_sensing.get_bresenham_lines(robot_coord, sensor_readout_coordinates)

            for bresenham_line in bresenham_lines:
                # Calculate the distance from the robot coordinate to the end point of each Bresenham line
                dist = calculate_distance(bresenham_line[-1][0],bresenham_line[-1][1],robot_row,robot_col)
                #                          bresenham_lines[len(bresenham_lines) - 1][1],robot_row,robot_col)
                #print(dist)
                for coordinate in bresenham_line:
                    if math.floor(coordinate[0]) < nRows and math.floor(coordinate[1]) < nCols and \
                       math.floor(coordinate[0]) > 0 and math.floor(coordinate[1]) > 0:
                        occupancy_grid[math.floor(coordinate[0])][math.floor(coordinate[1])] = 0


                    #if(dist<30):
                    #    occupancy_grid[math.floor(bresenham_line[-1][0])][math.floor(bresenham_line[-1][1])] = 15

            #for x in bresenham_lines:
            #for i in range(0, len(bresenham_lines)):
                # Traverse its elements
                #dist = calculate_distance(bresenham_lines[len(bresenham_lines) - 1][0],
                #                          bresenham_lines[len(bresenham_lines) - 1][1],robot_row,robot_col)

            #    for j in range(0, len(bresenham_lines[i])):
                    # Set their grid value to visited
            #        if math.floor(bresenham_lines[i][j][0]) < nRows and bresenham_lines[i][j][1] < nCols and\
            #                        math.floor(bresenham_lines[i][j][0]) > 0 and math.floor(bresenham_lines[i][j][1]) > 0:
            #            occupancy_grid[math.floor(bresenham_lines[i][j][0])][math.floor(bresenham_lines[i][j][1])] = 0
                    # Top line
                #    elif math.floor(bresenham_lines[i][j][0]) == 0 and bresenham_lines[i][j][1] > 0 and bresenham_lines[i][j][1] < nRows :
                #        occupancy_grid[math.floor(bresenham_lines[i][j][0])][math.floor(bresenham_lines[i][j][1])] = 15
                    # Left line
                #    elif math.floor(bresenham_lines[i][j][1]) == 0 and bresenham_lines[i][j][0] > 0 and bresenham_lines[i][j][0] < nRows :
                #        occupancy_grid[math.floor(bresenham_lines[i][j][0])][math.floor(bresenham_lines[i][j][1])] = 15
                    # Bottom line
                #    elif math.floor(bresenham_lines[i][j][1]) == 0 and bresenham_lines[i][j][0] > 0 and bresenham_lines[i][j][0] < nCols:
                #        occupancy_grid[math.floor(bresenham_lines[i][j][0])][math.floor(bresenham_lines[i][j][1])] = 15
                    # Right line
                #    elif math.floor(bresenham_lines[i][j][0]) == 0 and bresenham_lines[i][j][1] > 0 and bresenham_lines[i][j][1] < nCols:
                #        occupancy_grid[math.floor(bresenham_lines[i][j][0])][math.floor(bresenham_lines[i][j][1])] = 15

                    #if math.floor(bresenhamLines[i][len(bresenhamLines[i])]) - 1][0]) < nRows and math.floor(bresenhamLines[i][len(bresenhamLines[i]) - 1][0]) < nCols and \
                    #        math.floor(bresenhamLines[i][len(bresenhamLines[i])]) > 0 and math.floor(bresenhamLines[i][len(bresenhamLines[i])]) > 0:
                    #if math.floor(bresenham_lines[i][len(bresenham_lines[i]) - 1][0]) < nRows and \
                    #    math.floor(bresenham_lines[i][len(bresenham_lines[i]) - 1][1]) < nCols and \
                    #     math.floor(bresenham_lines[i][len(bresenham_lines[i]) - 1][0]) > 0 and \
                    #      math.floor(bresenham_lines[i][len(bresenham_lines[i]) - 1][1]) > 0:
                    #    occupancy_grid[math.floor(bresenham_lines[i][len(bresenham_lines[i]) - 1][0])][math.floor(bresenham_lines[i][len(bresenham_lines[i]) - 1][1])] = 15

            # Update the map

            frontier_calculator.find_frontiers(occupancy_grid, robot_coord)

            map.updateMap(occupancy_grid, maxVal, robot_row, robot_col, orientation)

    except UnexpectedResponse as ex:
        print('Unexpected response from server when sending speed commands:', ex)

