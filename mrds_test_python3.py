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
import numpy as np

from robot import postSpeed, getLaser, getLaserAngles, getPose, getHeading, laserValuesToCoordinates, \
    bresenham,getOrientation
from show_map import createmap, ShowMap, pos_to_grid
from math import pi
import math
import time
from math import log
import matplotlib.pyplot as plt

url = 'http://localhost:50000'
# HTTPConnection does not want to have http:// in the address apparently, so lest's remove it:
MRDS_URL = url[len("http://"):]
HEADERS = {"Content-type": "application/json", "Accept": "text/json"}


class UnexpectedResponse(Exception):
    pass


if __name__ == '__main__':

    showGUI = True  # set this to False if you run in putty
    # use the same no. of rows and cols in map and grid:
    nRows = 60
    nCols = 65
    # Initialize a ShowMap object. Do this only once!!
    map = ShowMap(nRows, nCols, showGUI)
    # create a grid with all cells set to 7 (unexplored) as numpy matrix:
    grid = np.ones(shape=(nRows, nCols)) * 7
    # or as a two-dimensional array:
    # grid = [[7 for col in range(nCols)] for row in range(nRows)]
    # create some obstacles (black/grey)
    # Upper left side:
    grid[0][0] = 15
    grid[0][1] = 15
    grid[0][2] = 15
    grid[0][3] = 15
    grid[0][4] = 15
    grid[0][5] = 15
    grid[0][6] = 15
    grid[0][7] = 15

    # Lower right side:
    grid[59][64] = 15
    grid[58][64] = 15
    grid[57][64] = 15
    grid[56][64] = 15
    grid[55][64] = 15

    # Lower left side:
    grid[59][0] = 12
    grid[59][1] = 11
    grid[59][2] = 10
    grid[59][3] = 9
    grid[59][4] = 8

    # An explored area (white)
    for rw in range(35, 50):
        for cl in range(32, 55):
            grid[rw][cl] = 7

    # Max grid value
    maxVal = 15

    # Hard coded values for max/min x,y
    min_x = -15
    max_y = 17
    cell_size = 1

    # Position of the robot in the grid (red dot)
    pose = getPose()
    curr_pos = pose['Pose']['Position']
    robot_coord = pos_to_grid(curr_pos['X'], curr_pos['Y'], min_x, max_y, cell_size)
    robot_row = robot_coord[0]
    robot_col = robot_coord[1]

    print('Sending commands to MRDS server', MRDS_URL)


    try:
        print('Telling the robot to go straight ahead.')
        response = postSpeed(0.1, 0.1)

        while(1):
            #
            # print("while")
            time.sleep(0.05)

            laser = getLaser()
            laserAngles = getLaserAngles()


            # Let's update the map again. You should update the grid and the position
            # In your solution you should not sleep of course, but update continuously
            pose = getPose()
            curr_pos = pose['Pose']['Position']
            robot_coord = pos_to_grid(curr_pos['X'], curr_pos['Y'], min_x, max_y, cell_size)
            robot_row = robot_coord[0]
            robot_col = robot_coord[1]

            # Retrieve the angles needed to calculate
            orientation=getOrientation();

            #Calculate the coordinates laser point readings
            endPoints = laserValuesToCoordinates(robot_coord,laser['Echoes'], laserAngles,orientation)

            #for x in range(0, len(endPoints)):

            #print(endPoints[0][0])
            #print(endPoints[0][1])


                #print(x)# OK!, goes from 0 - 270


            bresenhamLines = []

            # For each laser beam
            for x in range(0,len(endPoints)):
                # Calculate its line by Bresenham's algorithm
                bresenhamLine=list(bresenham(robot_row, robot_col, endPoints[x][0], endPoints[x][1]))
                #print(bresenhamLine)
                print("\n")

                # Append it to the Bresenham's lines list
                bresenhamLines.append(bresenhamLine)
                # For each line

            for i in range(0, len(bresenhamLines)):
                # Traverse its elements
                for j in range(0, len(bresenhamLines[i])):
                    # Set their grid value to visited
                    if math.floor(bresenhamLines[i][j][0]) < nRows and bresenhamLines[i][j][1] < nCols and\
                                    math.floor(bresenhamLines[i][j][0]) > 0 and math.floor(bresenhamLines[i][j][1]) > 0:
                        grid[math.floor(bresenhamLines[i][j][0])][math.floor(bresenhamLines[i][j][1])] = 0
                    # Top line
                    elif math.floor(bresenhamLines[i][j][0]) == 0 and bresenhamLines[i][j][1] > 0 and bresenhamLines[i][j][1] < nRows :
                        grid[math.floor(bresenhamLines[i][j][0])][math.floor(bresenhamLines[i][j][1])] = 15
                    # Left line
                    elif math.floor(bresenhamLines[i][j][1]) == 0 and bresenhamLines[i][j][0] > 0 and bresenhamLines[i][j][0] < nRows :
                        grid[math.floor(bresenhamLines[i][j][0])][math.floor(bresenhamLines[i][j][1])] = 15
                    # Bottom line
                    elif math.floor(bresenhamLines[i][j][1]) == 0 and bresenhamLines[i][j][0] > 0 and bresenhamLines[i][j][0] < nCols:
                        grid[math.floor(bresenhamLines[i][j][0])][math.floor(bresenhamLines[i][j][1])] = 15
                    # Left line
                    elif math.floor(bresenhamLines[i][j][0]) == 0 and bresenhamLines[i][j][1] > 0 and bresenhamLines[i][j][1] < nCols:
                        grid[math.floor(bresenhamLines[i][j][0])][math.floor(bresenhamLines[i][j][1])] = 15


            # Update the map
            map.updateMap(grid, maxVal, robot_row, robot_col, endPoints, orientation)

        #print('Waiting for a while...')
        time.sleep(20)
        print('Telling the robot to go in a circle.')
        response = postSpeed(0.9, 0.1)
    except UnexpectedResponse as ex:
        print('Unexpected response from server when sending speed commands:', ex)

    try:
        laser = getLaser()
        laserAngles = getLaserAngles()
        print(
            'The rightmost laser beam has angle %.3f deg from x-axis (straight forward) and distance %.3f '
            'meters.createMap' % (
                laserAngles[0], laser['Echoes'][0]
            ))

        print('Beam 1: %.3f Beam 269: %.3f Beam 270: %.3f' % (
            laserAngles[0] * 180 / pi, laserAngles[269] * 180 / pi, laserAngles[270] * 180 / pi))
    except UnexpectedResponse as ex:
        print('Unexpected response from server when reading laser data:', ex)

    try:
        pose = getPose()
        print('Current position: ', pose['Pose']['Position'])
        print('------- Laser values ------')
        for t in range(10):
            print('Current heading vector: X:{X:.3}, Y:{Y:.3}'.format(**getHeading()))
            laser = getLaser()
            print('Distance %.3f meters.' % (laser['Echoes'][135]))
            if laser['Echoes'][135] < 0.3:
                print('Danger! Brace for impact! Hit the brakes!')
                response = postSpeed(0, -0.1)
            time.sleep(1)
        postSpeed(0, 0)
        print("I'm done here!")
    except UnexpectedResponse as ex:
        print('Unexpected response from server when reading position:', ex)
