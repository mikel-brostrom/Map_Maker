from datetime import time
from math import sqrt, atan2, pi, cos

from reactiveLayer.sensing.robotMovement import get_heading, post_speed,\
     get_orientation, get_position


class PurePursuit:

    def get_position(self):
        pass

    def get_carrot_point(self, path, pos, look_ahead_distance):
        """Get the next goal point from the robot's position from a fixed look-a-head distance"""
        if path:
            for i in range(len(path)):
                # Get the coordinate on the top of the stack
                p = path[len(path) - 1]
                # Caculate the x and y distance from the actual
                # position to the carrot point
                dx = p['X'] - pos['X']
                dy = p['Y'] - pos['Y']
                # Calculate the distance
                h = self.pythagoras_theorem(dx, dy)
                if h < look_ahead_distance:
                    path.pop()
                else:
                    return p
        else:
            print("Stack failed")

    def pythagoras_theorem(self, x, y):
        """Pythagoras theorem"""
        return sqrt((x ** 2) + (y ** 2))

    def get_filtered_path(self, path, pos):
        """Get the next goal point from the robot's position from a fixed look-a-head distance"""
        min_distance = 100
        location = 0
        if path:
            for i in range(len(path)):
                # Get the coordinate on the top of the stack
                p = path[len(path) - i - 1]
                # Caculate the x and y distance from the actual
                # position to the carrot point
                dx = p['X'] - pos['X']
                dy = p['Y'] - pos['Y']
                # Calculate the distance
                h = self.pythagoras_theorem(dx, dy)
                # Update the location for the path coordinate
                # corresponding to the minimal distance
                if h < min_distance:
                    min_distance = h
                    location = i + 1

            # Pop everyting before this location
            for i in range(location):
                path.pop()

            return path

        else:
            print("Stack failed")

    def get_orientation(self):
        """Calculate vehicle orientation with respect to the global coordinate system"""
        # Get the XY Orientation as a bearing unit vector"""
        heading = get_heading()
        # Extract the x and y component
        hx = heading['X']
        hy = heading['Y']
        # Calculate the angle in radians, [-pi,pi]
        orientation = atan2(hy, hx)
        return orientation

    def robot_look_ahead(self, dx, dy):
        """Calculate look ahead angle: The angle between the carrot point and the world coordinate system"""
        lookAheadAngle = atan2(dy, dx)
        return lookAheadAngle

    def tranform_to_vcs(self, actual_coord, carrot_coord):
        """Convert a coordinate to the vehicles's coordinate system"""
        # Calculate distance to the goal point from the robot
        dx = carrot_coord['X'] - actual_coord['X']
        dy = carrot_coord['Y'] - actual_coord['Y']
        h = self.pythagoras_theorem(dx, dy)
        # Retrieve the angles needed to calculate alfa
        orientation_angle = get_orientation()
        look_ahead_angle = self.robot_look_ahead(dx, dy)
        # Calculate the angle from the vehicle to the carrot point in the
        # vehicle's coordinate system
        alfa = pi / 2 - orientation_angle + look_ahead_angle
        # Calculate the distance to the carrot points in the vehicle's
        # coordinate system
        delta_x = h * cos(alfa)
        return (delta_x, h)

    def calculate_curvature(self, deltaX, h):
        """ Calculate the curvature between the vehicle and the carrot point """
        # Calculate the curvature
        curvature = -(2 * deltaX) / (h ** 2)
        return curvature

    def init_orientation(self, path, look_ahead_distance):
        """ Orientates the vehicle thowards the first coordinata in the given path """

        # Determine the current location of the vehicle

        actual_coord = get_position()

        # Find the point on the path closest to the vehicle
        carrotPoint = self.get_carrot_point(path, actual_coord, look_ahead_distance)

        # Calculate distance to the goal point from the robot
        dx = carrotPoint['X'] - actual_coord['X']
        dy = carrotPoint['Y'] - actual_coord['Y']

        # Initialize values
        orientation_angle = get_orientation()
        look_ahead_angle = self.robot_look_ahead(dx, dy)

        angleDiff = look_ahead_angle - orientation_angle

        while ((angle_diff > 1) or (angle_diff < -1)):
            # Update values
            orientation_angle = get_orientation()
            look_ahead_angle = self.robot_look_ahead(dx, dy)
            angle_diff = look_ahead_angle - orientation_angle
            post_speed(-1, 0)
            time.sleep(0.01)
        return

