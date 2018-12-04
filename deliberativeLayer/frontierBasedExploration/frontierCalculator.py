import asyncio
from collections import deque


MIN_NUM_FRONTIER_POINTS = 30
OPEN_THRESHOLD = 0.2


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


    def find_frontiers(self, occupancy_grid, robot_global_pos):
        # Algorithm from https://arxiv.org/ftp/arxiv/papers/1806/1806.03581.pdf

        """
        Marking lists
        """
        frontiers=[]
        map_open_list = []
        map_close_list = []
        frontier_open_list = []
        frontier_close_list = []

        queue_m = deque([])
        queue_m.append(robot_global_pos)
        map_open_list.append(robot_global_pos)

        while queue_m:
            p = queue_m.popleft()
            if p in map_close_list:
                continue
            if self.is_frontier_point(p, occupancy_grid):
                queue_f = deque([])
                new_frontier = []

                queue_f.append(robot_global_pos)
                frontier_open_list.append(p)

                while queue_f:
                    q = queue_f.popleft(robot_global_pos)
                    if q in map_close_list and q in frontier_close_list:
                        continue
                    if self.is_frontier_point(q, occupancy_grid):
                        new_frontier.add(q)
                        for w in self.adjacent(q):
                            if w not in frontier_open_list and w not in frontier_close_list and w\
                            not in map_close_list:
                                queue_f.append(w)
                                frontier_open_list.add(w)
                    frontier_close_list.add(q)
                frontiers.add(new_frontier)
                frontier_close_list.add(new_frontier)
            for v in self.adjacent(p):
                if v not in map_open_list and v not in map_close_list and self.v_has_open_neighbour:
                    queue_m.append(w)
                    map_open_list.append(v)
            map_close_list.append(p)

        return frontiers

