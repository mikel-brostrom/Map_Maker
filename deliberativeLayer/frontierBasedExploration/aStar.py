import numpy as np
import heapq
import math


class PathPlanner:

    def neighbour(self, cell,c_space):
        row = cell[0]
        col = cell[1]
        neighbours = []

        for i in range(-1,2):
            for j in range(-1,2):
                neighbour = (row + i, col + j)

                if i == 0 and j == 0:
                    continue
                if c_space.is_within_grid(neighbour[0], neighbour[1]):
                    neighbours.append(neighbour)
        return neighbours

    def print_map(self):

        for row in range(0, self.map.shape[0]):
            for col in range(0, self.map.shape[1]):
                print("{:.1f}".format((self.map[row][col])), end=' ')
            print()

    def cost(self, current, next, grid):

        #Object detected
        if grid[next[0]][next[1]] == 1:
            heuristic_const = 100
        else:
            heuristic_const = 100

        dx = abs(current[0] - next[0])
        dy = abs(current[1] - next[1])
        return heuristic_const * math.sqrt(dx * dx + dy * dy)

    def set_coordinate(self, row, col, val):
        self.map[row][col] = val

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star_search(self, start, goal, c_space):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for neighbour in self.neighbour(current, c_space):
                new_cost = cost_so_far[current] + self.cost(current, neighbour, c_space.occupancy_grid)

                if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                    cost_so_far[neighbour] = new_cost
                    priority = new_cost + self.heuristic(goal, neighbour)
                    frontier.put(neighbour, priority)
                    came_from[neighbour] = current

        return came_from, cost_so_far

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)  # optional
        #path.reverse()  # optional
        return path


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]





#####################
# Testing for a small grid
#####################
# map = grid(10,10)
# start, goal = (1, 4), (7, 8)
# came_from, cost_so_far = a_star_search(map, start, goal)
# path = reconstruct_path(came_from, start, goal)

#####################
# Print cost on map
#####################
"""
print(cost_so_far)
for coord in cost_so_far:
    map.set_coordinate(coord[0], coord[1], cost_so_far[coord])

print()
map.print_map()
"""
#####################


#####################
# Print path on map
#####################
"""
for cell in path:
    print(cell)
    map.set_coordinate(cell[0], cell[1], 1.0)

print()
map.print_map()
"""
#####################

