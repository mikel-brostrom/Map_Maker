import numpy as np


class Cspace:
    """
    cspace information
    """
    def __init__(self, x_min, y_min, x_max, y_max, cell_size):
        """
        :param x1: x coordinate of top left corner of the area to explore
        :param y1: y coordinate of top left corner of the area to explore
        :param x2: x coordinate of bottom right corner of the area to explore
        :param y2: y coordinate of top left corner of the area to explore
        :param scale: resolution, i.e the number of cspace cells per real world meter
        """
        # The size of the cell in c_space
        self.cell_size = cell_size
        # The scaling needed to comply with the cell size
        self.scale = 1 / cell_size

        # Lower left corner coordinate
        self.x_min = x_min
        self.y_min = y_min

        # Upper right corner coordinate
        self.x_max = x_max
        self.y_max = y_max

        # c_space width
        self.c_space_width = x_max - x_min
        self.c_space_height = y_max - y_min

        # Get number of grid rows and column
        self.grid_nr_rows = int(self.c_space_width * self.scale)
        self.grid_nr_cols = int(self.c_space_height * self.scale)

        # Create probability grid
        self.occupancy_grid = np.ones(shape=(self.grid_nr_rows, self.grid_nr_cols)) * 0.5
        self.expanded_occupancy_grid = self.occupancy_grid

    def is_within_grid(self, x, y):
        return 0 <= x < self.grid_nr_rows and 0 <= y < self.grid_nr_cols

    def neighbour(self, coordinate):
        row = coordinate[0]
        col = coordinate[1]
        neighbours = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbour = (row + i, col + j)

                if i == 0 and j == 0:
                    continue

                if self.is_within_grid(row + i, col + j):
                    continue

                neighbours.append(neighbour)
        return neighbours

    def get_grid_nr_rows(self):
        return self.grid_nr_rows

    def get_grid_nr_cols(self):
        return self.grid_nr_cols

    def calculate_expanded_occupancy_grid(self):
        self.expanded_occupancy_grid = self.occupancy_grid.copy()
        for i in range(0, self.grid_nr_rows, 3):
            for j in range(0, self.grid_nr_cols, 3):
                if self.occupancy_grid[i][j] >= 0.3:
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            if self.is_within_grid(i + k, j + l):
                                self.expanded_occupancy_grid[i + k][j + l] = 1

    def print_cspace(self):

        for row in range(0, self.occupancy_grid.shape[0]):
            for col in range(0, self.occupancy_grid.shape[1]):
                print("{:.1f}".format((self.occupancy_grid[row][col])), end=' ')

            print()

