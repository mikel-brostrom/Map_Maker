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
import sched

from bayes.Bayesian import Bayesian
from deliberativeLayer.cartographer.map_info import Cspace
from deliberativeLayer.cartographer.show_map import *
from deliberativeLayer.frontierBasedExploration.frontierCalculator import *
from deliberativeLayer.frontierBasedExploration.aStar import *
from reactiveLayer.sensing.robotMovement import *
from reactiveLayer.sensing.robotSensing import *
from reactiveLayer.pathTracking.purePursuit import *
import time

url = 'http://localhost:50000'
# HTTPConnection does not want to have http:// in the address apparently, so lest's remove it:
MRDS_URL = url[len("http://"):]
HEADERS = {"Content-type": "application/json", "Accept": "text/json"}


# s = sched.scheduler(time.time, time.sleep)

class UnexpectedResponse(Exception):
    pass

class MissionPlanner:

    def __init__(self):
        self.showGUI = True  # set this to False if you run in putty
        # Max grid value
        self.maxVal = 15
        self.cell_size = 0.5
        self.path = []
        self.path_follower = PurePursuit()
        self.c_space = Cspace(-30, -30, 30, 30, self.cell_size)
        self.bayes_map = Bayesian(self.c_space.occupancy_grid, self.cell_size)
        self.map = ShowMap(self.c_space.grid_nr_rows, self.c_space.grid_nr_cols, self.showGUI, self.cell_size)
        self.robot_sensing = robotSensing()
        self.frontier_calculator = Frontier_calculator(40)
        self.path_planner = PathPlanner()
        self.pure_pursuit = PurePursuit()
        self.linear_speed = 1
        self.look_ahead_distance = 3 / self.cell_size


    def calculate_distance(self, x1, y1, x2, y2):
        return (abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2) ** 0.5

    def update_occupancy_grid(self):
        # Get all the laser readout values starting from
        # the one with angle 0 to 270 (in meters)
        laser_scan_values = self.robot_sensing.get_laser_scan()

        # Get all the laser angles starting from 0 to 270
        laser_angles = self.robot_sensing.get_laser_angles()

        # Converts the car's (x, y) position to (row, col) coordinate in the grid
        pose = get_pose()
        curr_pos = pose['Pose']['Position']

        robot_coord = pos_to_grid(curr_pos['X'], curr_pos['Y'], self.c_space.x_min, self.c_space.y_max, self.cell_size)
        robot_row = robot_coord[0]
        robot_col = robot_coord[1]
        # print('Im at coordinate', robot_coord) # These are floats! Not integers!

        # Retrieve the angles needed to calculate
        orientation = get_orientation()

        # Calculate the coordinates laser point readings

        sensor_readout_coordinates = self.robot_sensing.get_sensor_readout_coordinates(robot_coord,
                                                                                  laser_scan_values['Echoes'],
                                                                                  laser_angles, orientation,
                                                                                       self.cell_size)

        # Get all the Bresenham lines
        bresenham_lines = self.robot_sensing.get_bresenham_lines(robot_coord, sensor_readout_coordinates)

        for bresenham_line in bresenham_lines:
            self.bayes_map.bayes_handler(bresenham_line, robot_row, robot_col, self.c_space.get_grid_nr_rows(),
                                         self.c_space.get_grid_nr_cols())


    def update_path(self):

        ##########################
        # Calculates a new path when old one i followed or object detected
        ##########################
        path_planner.path_problem_detection(mission_planner)

        if not self.path or object_detected:

            response = post_speed(0, 0)
            frontiers = frontier_calculator.find_frontiers(c_space, robot_coord)

            # If no frontiers found, decrese the minium points required until frontier detected
            while not frontiers or (frontier_calculator.min_num_frontier_points == 2):
                frontier_calculator.change_frontier_attr()
                frontiers = frontier_calculator.find_frontiers(c_space, robot_coord)

                if frontier_calculator.min_num_frontier_points == 2 and len(frontiers) == 0:
                    print("Explored as much as possible, no more frontiers to be found for minimal val")
                    post_speed(0.3, 0)
            # frontier_calculator.change_frontier_attr()

            f = frontiers[0]
            print("Goal:", f)
            f1 = math.floor(f[0])
            f2 = math.floor(f[1])
            goal = (f1, f2)

            robot_row = math.floor(robot_coord[0])
            robot_col = math.floor(robot_coord[1])
            start = (robot_row, robot_col)
            path = path_planner.a_star(start, goal, c_space)
            #path = path_planner.reconstruct_path(came_from, start, goal)

            # Update to complete history of paths taken, only use for figures
            # map.update_complete_path(path)

            robot_coord = pos_to_grid(curr_pos['X'], curr_pos['Y'], c_space.x_min, c_space.y_max, cell_size)

            # Set the vehicle to point in the right direction from the beginning
            pure_pursuit.init_orientation(path, look_ahead_distance, robot_coord)

            ##########################################################################################
            # Not fixed
            ##########################################################################################

    ######################
        if len(path) >= 1:
            carrot_coordinate = pure_pursuit.get_carrot_point(path, robot_coord, look_ahead_distance)

            if carrot_coordinate:
                # Transform coordinates system to vehicle coordinate system
                vcs = pure_pursuit.tranform_to_vcs(robot_coord, carrot_coordinate)

                # Calculate the curvature of the circular arc
                curvature = pure_pursuit.calculate_curvature(vcs[0], vcs[1])

                # Calculate angular speed
                angularSpeed = curvature * linear_speed

                # Apply angular and linear speed to the vehicle
                post_speed(angularSpeed, linear_speed)
                # else:
                #    post_speed(0, 0)

        map.updateMap(self.c_space.occupancy_grid, maxVal, robot_row, robot_col, orientation, frontiers, path)


except UnexpectedResponse as ex:
    print('Unexpected response from server when sending speed commands:', ex)

