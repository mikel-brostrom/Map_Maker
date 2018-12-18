
from collections import deque

import math



# Maximum value for considering a grid coordinate open
OPEN_THRESHOLD = 0.4


class Frontier_calculator:
    """
    This class calculates the frontier out of a probability gris
    """
    def __init__(self, min_num_frontier_points):
        # Minimum number of coordinates in a frontier in order to consider it as a possible frontier
        self.min_num_frontier_points = min_num_frontier_points


    def find_frontiers(self, c_space, robot_coord):
        """
        Calculates all the frontier out of a probability grid

        Algorithm from: Frontier Based Exploration for Autonomous Robot
        https://arxiv.org/ftp/arxiv/papers/1806/1806.03581.pdf and
        Robot Exploration with Fast Frontier Detection: Theory and Experiments
        http://www.ifaamas.org/Proceedings/aamas2012/papers/3A_3.pdf

        Args
            c_space: the configuration space describing the environment
            robot_coord: the start coordinate for the BFS
        Return
            a list of lists which contains points describing each frontier
        """

        frontiers = []
        map_open_list = []
        map_close_list = []
        frontier_open_list = []
        frontier_close_list = []

        robot_coord = [math.floor(robot_coord[0]), math.floor(robot_coord[1])]

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
                queue_f.append(p)
                frontier_open_list.append(p)

                while queue_f:

                    q = queue_f.popleft()

                    if q in map_close_list and q in frontier_close_list:
                        continue

                    if self.is_frontier_point(q, c_space):
                        new_frontier.append(q)

                        for w in self.adjacent(q, c_space):
                            if w not in frontier_open_list and w not in frontier_close_list and w\
                              not in map_close_list:
                                queue_f.append(w)
                                frontier_open_list.append(w)

                    frontier_close_list.append(q)

                if len(new_frontier) > self.min_num_frontier_points:
                    frontiers.append(new_frontier)
                    frontier_close_list.append(new_frontier)

            for v in self.adjacent(p, c_space):
                if v not in map_open_list and v not in map_close_list and self.has_open_neighbor(v, c_space):
                    queue_m.append(v)
                    map_open_list.append(v)

            map_close_list.append(p)

        return self.frontiers_to_centroid(frontiers, c_space)

    def has_open_neighbor(self, p, c_space):
        """
        Returns True if the coordinate has an open neighbor

        Args
            c_space: the configuration space describing the environment
        Return
            a boolean value that indicates whether a coordinate has an open neighbor or not
        """
        #if not c_space.is_within_grid(p[0], p[1]):
        #    return False

        neighbors = self.adjacent(p, c_space)

        for x, y in neighbors:
            if c_space.occupancy_grid[x][y] <= OPEN_THRESHOLD:
                return True

        return False

    def adjacent(self, p, c_space):
        """
        Retrieves all the coordinates adjacent to another coordinate

        Args
            c_space: the configuration space describing the environment
        Return
            a list of tuples describing the coordinates adjacent to the input coordinate
        """

        adjacent_points = []

        #   _ _ _
        #  |_|_|_|
        #  |_|_|_|  (-1, -1)
        #  |X|_|_|
        if c_space.is_within_grid(p[0]-1, p[1]-1):
            adjacent_points.append((p[0] - 1, p[1]-1))
        #   _ _ _
        #  |_|_|_|
        #  |_|_|_|  (-1, 0)
        #  |_|X|_|
        if c_space.is_within_grid(p[0] - 1, p[1]):
            adjacent_points.append((p[0] - 1, p[1]))
        #   _ _ _
        #  |_|_|_|
        #  |_|_|_|  (-1, 1)
        #  |_|_|X|
        if c_space.is_within_grid(p[0] - 1, p[1]+1):
            adjacent_points.append((p[0] - 1, p[1]+1))
        #   _ _ _
        #  |_|_|_|
        #  |X|_|_|  (0, -1)
        #  |_|_|_|
        if c_space.is_within_grid(p[0], p[1]-1):
            adjacent_points.append((p[0], p[1]-1))
        #   _ _ _
        #  |_|_|_|
        #  |_|_|X|  (0, 1)
        #  |_|_|_|
        if c_space.is_within_grid(p[0], p[1]+1):
            adjacent_points.append((p[0], p[1]+1))
        #   _ _ _
        #  |X|_|_|
        #  |_|_|_|  (1, -1)
        #  |_|_|_|
        if c_space.is_within_grid(p[0] + 1, p[1]-1):
            adjacent_points.append((p[0] + 1, p[1]-1))
        #   _ _ _
        #  |_|X|_|
        #  |_|_|_|  (1, 0)
        #  |_|_|_|
        if c_space.is_within_grid(p[0] + 1, p[1]):
            adjacent_points.append((p[0] + 1, p[1]))
        #   _ _ _
        #  |_|_|X|
        #  |_|_|_|  (1, 1)
        #  |_|_|_|
        if c_space.is_within_grid(p[0] + 1, p[1]+1):
            adjacent_points.append((p[0] + 1, p[1]+1))

        return adjacent_points

    def is_frontier_point(self, p, c_space):
        """
        Any open cell adjacent to an unknown cell is labeled frontier edge cell.
        In order to consider a coordinate unknown its probability should be 0.5, the
        value the probability grid is initiated to

        Args
            c_space: the frontiers found in the probability gris
        Return
            a boolean value indicating whether the coordinate is a frontier point or not
        """
        #if not c_space.is_within_grid(p[0], p[1]):
        #    return False

        adjacent_points_to_p = self.adjacent(p, c_space)

        # If p is an open coordinate
        if c_space.occupancy_grid[p[0]][p[1]] <= OPEN_THRESHOLD:
            # And has an adjacent unknown cell
            for x, y in adjacent_points_to_p:
                if 0.30 <= c_space.expanded_occupancy_grid[x, y] <= 0.7:
                    return True

        return False

    def frontiers_to_centroid(self, frontiers, c_space):
        """
        Get the list of frontiers and calculate their centroid

        Args
            frontiers: the frontiers found in the probability grid
        Return
            a list of tuples describing the centroid of each frontier
        """
        sum_x = 0
        sum_y = 0
        frontier_centroid_list = []
        for frontier in frontiers:
            for x,y in frontier:
                sum_x += x
                sum_y += y
            length = len(frontier)
            # print('<frontiers_to_centroid>', length)
            if c_space.occupancy_grid[math.floor(sum_x/length)][math.floor(sum_y/length)] < 0.3:
                frontier_centroid_list.append((math.floor(sum_x/length), math.floor(sum_y/length)))

            sum_x = 0
            sum_y = 0

        return frontier_centroid_list

    def change_frontier_attr(self):
        #Could have input: min_num_frontier_points
        #self.min_num_frontier_points = min_num_frontier_points
        if self.min_num_frontier_points <= 10:
            self.min_num_frontier_points = 10
            return

        self.min_num_frontier_points = self.min_num_frontier_points/2
        print("No frontiers found, setting new frontier attr:", self.min_num_frontier_points)

