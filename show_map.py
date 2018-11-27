from  PIL import Image
import time
import threading
import numpy as np

from robot import getPose

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

        # remove the toolbar from plot
        plt.rcParams['toolbar'] = 'None'

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

    def updateMap(self, grid, maxvalue, robot_row, robot_col, endPoints):
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
                value = grid[row, col]
                # if value is <0 draw a gray pixel else mapping the value between 0 - 255
                # where 0 is black and 255 is white
                if value < 0:
                    # set pixel value to gray
                    self.__image.putpixel((col, row), 127)
                else:
                    # set pixel value
                    self.__image.putpixel((col, row), abs(value * 255 / maxvalue - 255))

        for x in range(0, len(endPoints)):
            # Calculate its line by Bresenham's algorithm
            if np.math.floor(endPoints[x][0]) < 60 and np.math.floor(endPoints[x][1]) < 65 and \
                    np.math.floor(endPoints[x][0]) > 0 and np.math.floor(endPoints[x][1]) > 0:
                self.__image.putpixel((np.math.floor(endPoints[x][0]), np.math.floor(endPoints[x][1])), 200)

        # update the plot withe new image
        self.__ax.clear()
        self.__implot = self.__ax.imshow(self.__image)

        # remove the x and y tick in figure
        self.__ax.set_xticks([])
        self.__ax.set_yticks([])

        # plot the robot pose
        self.__ax.plot((robot_col), (robot_row), 'rs', markersize=self.__robot_size)

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


def createmap():
    """"A simple example of how to use the ShowMap class """
    showGUI = True  # set this to False if you run in putty
    # use the same no. of rows and cols in map and grid:
    nRows = 60
    nCols = 65

    # Initialize a ShowMap object. Do this only once!!
    map = ShowMap(nRows, nCols, showGUI)
    # create a grid with all cells set to 7 (unexplored) as numpy matrix:
    grid = np.ones(shape=(nRows, nCols)) * 7
    # or as a two-dimensional array:
    # grid = [[7 for col in range(nCols)] for row in range(nRows)]

    # create some obstacles (black/grey)
    # Upper left side:
    grid[0][0] = 15
    grid[0][1] = 15
    grid[0][2] = 15
    grid[0][3] = 15
    grid[0][4] = 15
    grid[0][5] = 15
    grid[0][6] = 15
    grid[0][7] = 15

    # Lower right side:
    grid[59][64] = 15
    grid[58][64] = 15
    grid[57][64] = 15
    grid[56][64] = 15
    grid[55][64] = 15

    # Lower left side:
    grid[59][0] = 12
    grid[59][1] = 11
    grid[59][2] = 10
    grid[59][3] = 9
    grid[59][4] = 8

    # An explored area (white)
    for rw in range(35, 50):
        for cl in range(32, 55):
            grid[rw][cl] = 0

    # Max grid value
    maxVal = 15

    # Hard coded values for max/min x,y
    min_x = -15
    max_y = 17
    cell_size = 0.5

    # Position of the robot in the grid (red dot)
    pose = getPose()
    curr_pos = pose['Pose']['Position']
    robot_coord = pos_to_grid(curr_pos['X'], curr_pos['Y'], min_x, max_y, cell_size)
    robot_row = robot_coord[0]
    robot_col = robot_coord[1]

    # Update the map
    map.updateMap(grid, maxVal, robot_row, robot_col)
    print("Map updated")

    time.sleep(2)
    # Let's update the map again. You should update the grid and the position
    # In your solution you should not sleep of course, but update continuously
    pose = getPose()
    curr_pos = pose['Pose']['Position']
    robot_coord = pos_to_grid(curr_pos['X'], curr_pos['Y'], min_x, max_y, cell_size)
    robot_row = robot_coord[0]
    robot_col = robot_coord[1]
    map.updateMap(grid, maxVal, robot_row, robot_col)
    print("Map updated again")

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


