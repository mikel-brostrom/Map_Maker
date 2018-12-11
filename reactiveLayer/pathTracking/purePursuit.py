import time

from math import sqrt, atan2, pi, cos

from reactiveLayer.sensing.robotMovement import get_heading, post_speed,\
     get_orientation, get_position


class PurePursuit:

    def get_position(self):
        pass

    """
    def get_carrot_point(self, path, pos, look_ahead_distance):
        Get the next goal point from the robot's position from a fixed look-a-head distance
        if path:
 
            for i in range(len(path)):
                # Get the coordinate on the top of the stack
                #p = path[len(path) - 1]
                p = path[0]
                # Caculate the x and y distance from the actual
                # position to the carrot point
                dx = p[0] - pos[0]
                dy = p[1] - pos[1]
                # Calculate the distance
                h = self.pythagoras_theorem(dx, dy)

                if h < look_ahead_distance:
                    carrot_point= path.pop()
                    print("Popped val: Carrot point", carrot_point)
                else:
                    return p
        else:
            print("Stack failed")
    """
    def get_carrot_point(self, path, pos, look_ahead_distance):
        """Get the next goal point from the robot's position from a fixed look-a-head distance"""
        if path:
            p = path[len(path)-1]
            dx = p[0] - pos[0]
            dy = p[1] - pos[1]

            # Calculate the distance
            h = self.pythagoras_theorem(dx, dy)

            if h < look_ahead_distance:
                carrot_point = path.pop()
                #print("Popped val: Carrot point", carrot_point)
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

    def init_orientation(self, path, look_ahead_distance, current_position):

        # Find the point on the path closest to the vehicle
        post_speed(0, 0)
        carrot_point = self.get_carrot_point(path, current_position, look_ahead_distance)


        if not carrot_point:
            #print("No carrot")
            return
        # Calculate distance to the goal point from the robot
        dx = carrot_point[0] - current_position[0]
        dy = carrot_point[1] - current_position[1]

        # Initialize values
        look_ahead_angle = self.robot_look_ahead(dx, dy)
        orientation_angle = self.get_orientation()
        angle_diff = look_ahead_angle - orientation_angle

        print("Target angle:", angle_diff, "Angle limit before driving", pi / 16)
        while abs(angle_diff) > (pi / 16):

            orientation_angle = self.get_orientation()
            angle_diff = look_ahead_angle - orientation_angle

            if angle_diff > pi:
                post_speed(-0.8, 0)
            else:
                post_speed(0.8, 0)

            time.sleep(0.05)


