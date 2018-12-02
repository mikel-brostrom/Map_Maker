import asyncio
from collections import deque


class frontierCalculator:
    """
    This class is used to represent game positions. It uses a 2-dimensional char array for the board
    and a Boolean to keep track of which player has the move.

    Author: Ola Ringdahl
    """

    def seen_contour_getter(self, occupancy_grid, nRows, nCols):
        """Sends a speed command to the MRDS server"""
        #print('seen countour getter!')
        for i in range(0,nRows):
            for j in range(0,nCols):
                if occupancy_grid[i][j] == 7:
                    print('Unknown')


    def find_frontiers(self, cspace_map, robot_global_pos):
        # Algorithm from http://www.ifaamas.org/Proceedings/aamas2012/papers/3A_3.pdf

        map_open_list = []
        map_close_list = []
        frontier_open_list = []
        frontier_close_list = []

        queue_m = deque([])

        robot_global_pos = robot_global_pos

        queue_m.append(robot_global_pos)
        map_open_list.append(robot_global_pos)

        while queue_m:
            p = queue_m.popleft()
            if p in map_open_list:
                continue
            if p in frontier_open_list or p in frontier_close_list:
                queue_f = deque([])
                new_frontier = []

                queue_m.append(robot_global_pos)