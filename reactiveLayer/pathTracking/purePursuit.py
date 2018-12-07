from datetime import time
from math import sqrt, atan2, pi, cos

from reactiveLayer.sensing.robotMovement import getHeading, postSpeed, UnexpectedResponse, getOrientation

class PurePursuit:

    def getPosition(self):
        pass

    """Get the next goal point from the robot's position from a fixed look-a-head distance"""

    def get_carrot_point(self, path, pos, look_ahead_distance):
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

    """Pythagoras theorem"""
    def pythagoras_theorem(self, x, y):
        return sqrt((x ** 2) + (y ** 2))


    """Get the next goal point from the robot's position from a fixed look-a-head distance"""
    def get_carrot_point(self, path, pos, lookAeadDistance):
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
                if h < lookAeadDistance:
                    path.pop()
                else:
                    return p
        else:
            print("Stack failed")

    """Get the next goal point from the robot's position from a fixed look-a-head distance"""
    def get_filtered_path(self, path, pos):
        minDistance = 100
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
                if h < minDistance:
                    minDistance = h
                    location = i + 1

            # Pop everyting before this location
            for i in range(location):
                path.pop()

            return path

        else:
            print("Stack failed")

    """Calculate vehicle orientation with respect to the global coordinate system"""
    def get_orientation(self):
        # Get the XY Orientation as a bearing unit vector"""
        heading = getHeading()
        # Extract the x and y component
        hx = heading['X']
        hy = heading['Y']
        # Calculate the angle in radians, [-pi,pi]
        orientation = atan2(hy, hx)
        return orientation

    """Calculate look ahead angle: The angle between the carrot point and the world coordinate system"""

    def robot_look_ahead(self, dx, dy):

        lookAheadAngle = atan2(dy, dx)

        return lookAheadAngle

    """Convert a coordinate to the vehicles's coordinate system"""

    def tranform_to_vcs(self, actualCoord, carrotCoord):

        # Calculate distance to the goal point from the robot
        dx = carrotCoord['X'] - actualCoord['X']
        dy = carrotCoord['Y'] - actualCoord['Y']
        h = self.pythagoras_theorem(dx, dy)
        # Retieve the angles needed to calculate alfa
        orientationAngle = getOrientation()
        lookAheadAngle = self.robot_look_ahead(dx, dy)
        # Calculate the angle from the vehicle to the carrot point in the
        # vehicle's coordinate system
        alfa = pi / 2 - orientationAngle + lookAheadAngle
        # Caculate the distance to the carrot pointe in the vehicle's
        # coordinate system
        deltaX = h * cos(alfa)
        return (deltaX, h)

    """ Calculate the curvature between the vehicle and the carrot point """

    def calculate_curvature(self, deltaX, h):
        # Calculate the curvature
        curvature = -(2 * deltaX) / (h ** 2)
        return curvature

    """ Orientates the vehicle thowards the first coordinata in the given path """
    def init_orientation(self, path, lookAeadDistance):

        # Determine the current location of the vehicle

        actualCoord = getPosition()

        # Find the point on the path closest to the vehicle
        carrotPoint = self.get_carrot_point(path, actualCoord, lookAeadDistance)

        # Calculate distance to the goal point from the robot
        dx = carrotPoint['X'] - actualCoord['X']
        dy = carrotPoint['Y'] - actualCoord['Y']

        # Initialize values
        orientationAngle = getOrientation()
        lookAheadAngle = self.robot_look_ahead(dx, dy)

        angleDiff = lookAheadAngle - orientationAngle

        while ((angleDiff > 1) or (angleDiff < -1)):
            # Update values
            orientationAngle = getOrientation()
            lookAheadAngle = self.robot_look_ahead(dx, dy)
            angleDiff = lookAheadAngle - orientationAngle
            postSpeed(-1, 0)
            time.sleep(0.01)
        return

