import asyncio
from collections import deque

import math

from deliberativeLayer.cartographer import map_info

MIN_NUM_FRONTIER_POINTS = 30
OPEN_THRESHOLD = 0.2


class frontierCalculator:
    """
    This class is used to represent game positions. It uses a 2-dimensional char array for the board
    and a Boolean to keep track of which player has the move.

    Author: Ola Ringdahl
    """


    def find_frontiers(self, c_space, robot_coordt):
        # Algorithm from https://arxiv.org/ftp/arxiv/papers/1806/1806.03581.pdf

        """
        Marking lists
        """
        frontiers=[]
        map_open_list = []
        map_close_list = []
        frontier_open_list = []
        frontier_close_list = []

        x = math.floor(robot_coordt[0])
        y = math.floor(robot_coordt[1])

        #print(x, y)

        robot_coord = [x,y]

        queue_m = deque([])
        queue_m.append(robot_coord)
        map_open_list.append(robot_coord)

        while queue_m:
            p = queue_m.popleft()
            if p in map_close_list:
                continue
            if self.is_frontier_point(p, c_space):
                queue_f = deque([])
                new_frontier = []

                queue_f.append(robot_coord)
                frontier_open_list.append(p)

                while queue_f:
                    q = queue_f.popleft(robot_coord)
                    if q in map_close_list and q in frontier_close_list:
                        continue
                    if self.is_frontier_point(q, c_space.occupancy_grid):
                        new_frontier.add(q)
                        for w in self.adjacent(q):
                            if w not in frontier_open_list and w not in frontier_close_list and w\
                            not in map_close_list:
                                queue_f.append(w)
                                frontier_open_list.add(w)
                    frontier_close_list.add(q)
                frontiers.add(new_frontier)
                frontier_close_list.add(new_frontier)
            for v in self.adjacent(p, c_space):
                if v not in map_open_list and v not in map_close_list and self.has_open_neighbor(v, c_space):
                    queue_m.append(v)
                    map_open_list.append(v)
            map_close_list.append(p)

        return frontiers

    def has_open_neighbor(self, p, c_space):
        """
#        Returns True if point has an unknown cell adjacent to it
        """
        if not c_space.is_within_grid(p[0],p[1]):
            return False

        neighbors = self.adjacent(p, c_space)



        for p in neighbors:

            x, y = p

            if c_space.occupancy_grid[x][y] <= OPEN_THRESHOLD:
                return True

        return False


    def adjacent(self, p, c_space):
        """
        Returns the positions adjacent to the point.
        """

        x, y = p

        x_max = c_space.grid_nr_rows - 1

        y_max = c_space.grid_nr_columns - 1

        adjacent_points = set([])

        if x < x_max:
            adjacent_points.add((x + 1, y))

        if y < y_max:
            adjacent_points.add((x, y + 1))

        if x < x_max and y < y_max:
            adjacent_points.add((x + 1, y + 1))

        if x > 0:
            adjacent_points.add((x - 1, y))

        if y > 0:
            adjacent_points.add((x, y - 1))

        if x > 0 and y > 0:
            adjacent_points.add((x - 1, y - 1))

        if x < x_max and y > 0:
            adjacent_points.add((x + 1, y - 1))

        if x > 0 and y < y_max:
            adjacent_points.add((x - 1, y + 1))

        return adjacent_points

    def is_frontier_point(self, p, c_space):

        #print(p)
        if not c_space.is_within_grid(p[0],p[1]):
            return False

        x, y = p



        epsilon = 0.2

        if abs(c_space.occupancy_grid[p[0]][p[1]] - 0.5) > epsilon:

            return False



        for p in self.adjacent(p):

            x, y =  math.floor(p)

            if c_space.occupancy_grid[x, y] <= OPEN_THRESHOLD:

                return True



        return False

