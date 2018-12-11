from reactiveLayer.sensing.robotMovement import *
import time

def detect_object_front(point, laser, laser_2, cell_size):
    laser_front = laser_2[0]
    laser_left = laser_2[1]
    laser_right = laser_2[2]

    #print(point)
    #print(laser)
    #print(laser_2)
    #print(laser_front/cell_size)

    if laser_front/cell_size < 4:
        print("Object detected in front")
        post_speed(-0.2, -0.3)
        time.sleep(0.1)
        return 1
    if laser_left/cell_size < 4:
        print("Object detected in left")
        post_speed(-0.8, -0.2)
        time.sleep(0.1)
        return 1
    if laser_right/cell_size < 4:
        print("Object detected in right")
        post_speed(0.8, -0.2)
        time.sleep(0.1)
        return 1
