import time

from math import sqrt, atan2, pi, cos, degrees

from reactiveLayer.sensing.robotMovement import get_heading, post_speed,\
     get_orientation, get_position


class PurePursuit:

    def __init__(self):
        self.curr_carrot_point = 0
        self.init = False
        self.previous_dist_to_carrot = 0

    def get_carrot_point(self, path, pos, look_ahead_distance):
        """Get the next goal point from the robot's position from a fixed look-a-head distance"""
        if path:
            p = path[len(path)-1]
            dx = p[0] - pos[0]
            dy = p[1] - pos[1]

            # Calculate the distance
            h = self.pythagoras_theorem(dx, dy)

            if h < look_ahead_distance:
                path.pop()
                if path:
                    p = path[len(path) - 1]
                    return p
            else:
                return p
        else:
            print("Stack failed")

    def pythagoras_theorem(self, x, y):
        """Pythagoras theorem"""
        return sqrt((x ** 2) + (y ** 2))

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
        dx = carrot_coord[0] - actual_coord[0]
        dy = carrot_coord[1] - actual_coord[1]
        h = self.pythagoras_theorem(dx, dy)
        # Retrieve the angles needed to calculate alfa
        orientation_angle = get_orientation()+ pi/2
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

    """ Orientates the vehicle thowards the first coordinata in the given path """

    def init_orientation(self, path, look_ahead_distance, current_position, init):
        self.init = init

        #print("Init orient")
        # Find the point on the path closest to the vehicle
        post_speed(0, 0)
        self.curr_carrot_point = self.get_carrot_point(path, current_position, look_ahead_distance)
        print(self.curr_carrot_point)

        if not self.curr_carrot_point:
            #print("No carrot")
            return

        self.is_correct_angle( path, look_ahead_distance, current_position)

    def is_correct_angle(self, path, look_ahead_distance, current_position):

        self.curr_carrot_point = self.get_carrot_point(path, current_position, look_ahead_distance)

        if not self.curr_carrot_point:
            #print("No carrot")
            return

        dx = self.curr_carrot_point[0] - current_position[0]
        dy = self.curr_carrot_point[1] - current_position[1]
        distance = self.pythagoras_theorem(dx, dy)

        if distance <= 1.5:
            print(distance)


        #if distance > 2/0.1:
        #    if distance > self.previous_dist_to_carrot:
        #        self.previous_dist_to_carrot = distance
        #    self.previous_dist_to_carrot =
        #    print("Distance from closset path point is great, returruururururn")

        # Initialize values
        look_ahead_angle = self.robot_look_ahead(dx, dy)
        orientation_angle = self.get_orientation()
        angle_diff = look_ahead_angle - orientation_angle - pi/2

        if ( abs(angle_diff) > (pi / 3) ) and self.init is True:

            #print(angle_diff)
            if angle_diff > 0:
                post_speed(0.8*abs(angle_diff), 0)
            else:
                post_speed(-0.8*abs(angle_diff), 0)
        else:
            self.init = False
            return True

