import matplotlib.pyplot as plt
import numpy as np
from Bayesian import Bayesian
import math

grid_size = 10
prob_grid = np.array([[0.5 for col in range(grid_size)] for row in range(grid_size)])
print(prob_grid)

grid = 8
grid = np.array([[0 for col in range(grid)] for row in range(grid)])
line = grid[:][1]

line_x = np.ones(8)*4
line_x = line_x.astype(int)
line_y = np.arange(8)
bresenham_lines = list(zip(line_x, line_y))
print(bresenham_lines)

"""Vi antar att sensorn läser av relativt roboten"""
shit = Bayesian(prob_grid)
shit.bayes_handler(bresenham_lines)

########



class RegionDivider:
    def __init__(self, sensor_readings, cell):
        self.sensor_readings = sensor_readings

    def region_divider(self, cells):
        region = None

        if cell_to_robot_dist > object_to_robot_dist:
            return None

        if d_laser > d_cell:
            region = 1




for row in range(grid_size):
    for col in range(grid_size):
        plt.scatter(row, col)
        #grid[row][col]
#plt.show()

"""
P.conditioned(laser_reading, occupied)
P.conditioned(laser_reading, empty)
P.probability(occupied)
P.probability(empty)

# P(s|H)P(H)
# P(H|s):
P.bayes_rule()

print("bayesian", P.empty(3.5, math.radians(0)))
print("bayesian", P.occupied(3.5, math.radians(0)))
print("Total prob", P.empty(3.5, math.radians(0)) + P.occupied(3.5, math.radians(0)))
"""