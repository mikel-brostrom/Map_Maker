from reactiveLayer.sensing.robotMovement import *
import time


def detect_object_front(laser_readout_distances, cell_size):

    for i in range(0, len(laser_readout_distances)):
        if laser_readout_distances[i]/cell_size < 2/cell_size :
            if i < 135:
                print("Object detected to the right")
                post_speed(-0.5, -0.1)
                time.sleep(2)
                return 1
            else:
                print("Object detected to the left")
                post_speed(0.5, -0.1)
                return 1
