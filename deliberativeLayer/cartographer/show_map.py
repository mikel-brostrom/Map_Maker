import threading
import time

import numpy as np
from  PIL import Image

from reactiveLayer.sensing.robotMovement import get_pose

"""
ShowMap creates a Gui for showing the progress of the created map and saves it to file every 5 second
Author Peter Hohnloser
"""
class ShowMap(object):
    def __init__(self, gridHeight, gridWidth, showGUI):
        """
        Constructor for ShowMap

        Args:
            param gridHeight the height of the grid (no. of rows)
            param gridWidth the width of the grid (no. of columns)
            param ShowGUI if true showing the map
        """
        import matplotlib
        if not showGUI:
            matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        self.saveMapTime = 5.0
        self.mapName = 'map.png'
        self.first = True
        self.__robot_size = 6
        self.__size = (gridHeight, gridWidth)

        # create a grayscale image
        data = np.ones(shape=self.__size)
        self.__image = Image.fromarray(data * 0.5 * 255)

        fig_size = [8, 8]

        # remove the toolbar from plot
        plt.rcParams['toolbar'] = 'None'
        plt.rcParams["figure.figsize"] = fig_size

        # using matplotlib to show an image in a subplot
        self.__fig, self.__ax = plt.subplots(1, 1)
        self.__fig.suptitle('Show Map')

        # remove the x and y tick in figure
        self.__ax.set_xticks([])
        self.__ax.set_yticks([])

        # Show image window
        self.__implot = self.__ax.imshow(self.__image)

        plt.show(block=False)
        self.__fig.canvas.draw()

        saveMap(self.__fig, self.mapName)
        self.start_time = time.time()

    def updateMap(self, grid, maxvalue, robot_row, robot_col, orientation, frontiers, path_to_goal):
        """
        Creates a new BufferedImage from a grid with integer values between 0 - maxVal,
        where 0 is black and maxVal is white, with a grey scale in between. Negative values are shown as gray.
        Call this Method after you have updated the grid.

        Args:
            param grid is the updated grid (numpy matrix or a two-dimensional array)
            param maxVal is the max value that is used in the grid
            param robot_row is the current position of the robot in grid row
            param robot_col is the current position of the robot in grid column
        """
        # convert grid to a numpy matrix
        grid = np.matrix(grid)
        # mapping the grid to an Image
        for col in range(0, self.__size[1]):
            for row in range(0, self.__size[0]):
                value = grid[row, col]*15
                # if value is <0 draw a gray pixel else mapping the value between 0 - 255
                # where 0 is black and 255 is white
                if value < 0:
                    # set pixel value to gray
                    self.__image.putpixel((col, row), 127)
                else:
                    # set pixel value
                    self.__image.putpixel((col, row), abs(value * 255 / maxvalue - 255))

        # update the plot withe new image
        self.__ax.clear()
        self.__implot = self.__ax.imshow(self.__image)

        # remove the x and y tick in figure
        self.__ax.set_xticks([])
        self.__ax.set_yticks([])

        # plot the robot pose
        self.__ax.plot((robot_col), (robot_row), 'rs', markersize=self.__robot_size)
        # plot the robot heading
        self.__ax.plot((robot_col + 3 * np.sin(orientation + np.math.pi/2)), (robot_row + 3 * np.cos(orientation+ np.math.pi/2)), 'bs', markersize=self.__robot_size)

        for frontier in frontiers:
            self.__ax.plot(frontier[1], (frontier[0]), 'gs', markersize=3)

        for coordinates in path_to_goal:
            self.__ax.plot(coordinates[1], (coordinates[0]), 'ys', markersize=1)

        # draw new figure
        self.__fig.canvas.draw()

        # Start a time that saves the image ever n seconds
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.saveMapTime:
            self.t = threading.Thread(target=saveMap, args=(self.__fig, self.mapName,))
            self.t.start()
            self.start_time = time.time()

    def close(self):
        """ Saves the last image before closing the application """
        import matplotlib.pyplot as plt
        saveMap(self.__fig, self.mapName)
        plt.close()


def createmap():
    pass


def saveMap(fig, mapname):
    """ Saves the drawn Map to an Image """
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    img = Image.fromarray(data)
    img.convert('RGB').save(mapname, 'PNG')


def pos_to_grid(x, y, xmin, ymax, cellsize):
    """
    Converts an (x,y) positon to a (row,col) coordinate in the grid
    :param x: x-position
    :param y: y-position
    :param xmin: The minimum x-position in the grid
    :param ymax: The maximum y-position in the grid
    :param cellsize: the resolution of the grid
    :return: A tuple with (row,col)
    """
    col = (x - xmin) / cellsize
    row = (ymax - y) / cellsize
    return (row, col)


