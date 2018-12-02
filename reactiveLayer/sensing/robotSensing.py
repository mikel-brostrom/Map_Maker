import http.client, json
from math import pi
import math


url = 'http://localhost:50000'
# HTTPConnection does not want to have http:// in the address apparently, so lest's remove it:
MRDS_URL = url[len("http://"):]
HEADERS = {"Content-type": "application/json", "Accept": "text/json"}


class UnexpectedResponse(Exception):
    pass


class robotSensing:

    def get_laser_scan(self):
        """
        Requests the current laser scan from the
        MRDS server and parses it into a dict
        """
        mrds = http.client.HTTPConnection(MRDS_URL)
        mrds.request('GET', '/lokarria/laser/echoes')
        response = mrds.getresponse()
        if response.status == 200:
            laserData = response.read()
            response.close()
            return json.loads(laserData.decode())
        else:
            return response


    def get_laser_angles(self):
        """
        Requests the current laser properties from
        the MRDS server and parses it into a dict
        """
        mrds = http.client.HTTPConnection(MRDS_URL)
        mrds.request('GET', '/lokarria/laser/properties')
        response = mrds.getresponse()
        if response.status == 200:
            laserData = response.read()
            response.close()
            properties = json.loads(laserData.decode())
            beamCount = int((properties['EndAngle'] - properties['StartAngle']) / properties['AngleIncrement'])
            a = properties['StartAngle']  # +properties['AngleIncrement']
            angles = []
            while a <= properties['EndAngle']:
                angles.append(a)
                a += pi / 180  # properties['AngleIncrement']
            # angles.append(properties['EndAngle']-properties['AngleIncrement']/2)
            return angles
        else:
            raise UnexpectedResponse(response)

    def get_sensor_readout_coordinates(self,robot_coord, laser, laser_angles, orientation):
        """
        Requests the current laser properties from
        the MRDS server and parses it into a dict
        """
        coord_x = [0]*len(laser)
        coord_y = [0]*len(laser)

        for x in range(0,len(laser_angles)):
            coord_x[x] = robot_coord[0]+math.cos(laser_angles[x]+orientation)*laser[x]
            coord_y[x] = robot_coord[1]+math.sin(laser_angles[x]+orientation)*laser[x]

        result = zip(coord_x, coord_y)
        # Converting iterator to set
        resultSet = list(result)

        return resultSet


    def get_bresenham_lines(self,robot_coord, sensor_readout_coordinates):
        """
        Yield integer coordinates on the line from (x0, y0) to (x1, y1).
        Input coordinates should be integers.
        The result will contain both the start and the end point.
        """
        bresenhamLines = []

        # For each laser beam
        for x in range(0, len(sensor_readout_coordinates)):
            # Calculate its line by Bresenham's algorithm
            bresenhamLine = list(self.bresenham(robot_coord[0], robot_coord[1], sensor_readout_coordinates[x][0], sensor_readout_coordinates[x][1]))
            # print(bresenhamLine)
            # print("\n")

            # Append it to the Bresenham's lines list
            bresenhamLines.append(bresenhamLine)

        return bresenhamLines


    def bresenham(self,x0, y0, x1, y1):
        """
        Yield integer coordinates on the line from (x0, y0) to (x1, y1).
        Input coordinates should be integers.
        The result will contain both the start and the end point.
        """
        dx = math.floor(x1) - math.floor(x0)
        dy = math.floor(y1) - math.floor(y0)

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign

        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2*dy - dx
        y = 0

        for x in range(dx + 1):
            yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy

