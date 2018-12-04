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
        # The size of the cell in CSPACE
        self.cell_size = cell_size
        # The scaling needed to comply with the cell size
        self.scale = 1 / cell_size

        # Lower left corner coordinate
        self.x_min = x_min
        self.y_min = y_min

        # Upper right corner coordinate
        self.x_max = x_max
        self.y_max = y_max

        # CSAPCE width
        self.c_space_width = x_max - x_min
        self.c_space_height = y_max - y_min

        # Get number of grid rows and column
        self.grid_nr_rows = int(self.c_space_width * self.scale)
        self.grid_nr_columns = int(self.c_space_height * self.scale)

        # Create probability grid
        self.occupancy_grid = np.ones(shape=(self.grid_nr_rows, self.grid_nr_columns)) * 7

    def is_within_grid(self, x, y):
        return 0 <= x < self.grid_nr_rows and 0 <= y < self.grid_nr_columns
